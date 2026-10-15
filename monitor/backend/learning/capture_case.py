"""Generate actual general-service HTTP requests and export ONLY their resulting DB rows.

CMD: python -m learning.capture_case 12 > observation-next.json
No DB INSERT, fake JSON, or hardcoded event IDs are used.
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
import requests
from learning.support import get_latest_id, read_live_events


def capture_case(count: int, base_url: str | None = None):
    if count < 1 or count > 100:
        raise ValueError("Provide 1 to 100 actual list requests")
    base = (base_url or os.getenv("GENERAL_URL", "http://general-api:5000")).rstrip("/")
    before = get_latest_id()
    for _ in range(count):
        response = requests.get(base + "/", timeout=15)
        if response.status_code != 200:
            raise RuntimeError(f"General GET / returned HTTP {response.status_code}")
    missing = requests.get(base + "/training-missing", timeout=15)
    if missing.status_code != 404:
        raise RuntimeError(f"General missing route returned HTTP {missing.status_code}")
    rows = []
    for _ in range(40):
        rows, _ = read_live_events(before)
        selected = [r for r in rows if r["method"] == "GET" and r["path"] == "/" and r["status"] == 200 and r["event_type"] == "post_list"]
        errors = [r for r in rows if r["path"] == "/training-missing" and r["status"] == 404]
        if len(selected) >= count and errors:
            break
        time.sleep(0.25)
    else:
        raise RuntimeError("Requests were sent but the expected DB rows did not arrive; inspect general/monitor logs")
    serializable = [
        {**dict(r), "occurred_at": r["occurred_at"].isoformat() if isinstance(r["occurred_at"], datetime) else str(r["occurred_at"])}
        for r in rows
    ]
    return {"after_id": before, "requested_views": count, "original_rows": serializable}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("count", type=int, choices=[4, 10, 12])
    parser.add_argument("--url", default=None, help="Override for a reachable LOCAL general service")
    args = parser.parse_args()
    try:
        result = capture_case(args.count, args.url)
    except (requests.RequestException, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
