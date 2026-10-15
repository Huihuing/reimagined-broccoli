"""Create and forward the SAME HTTP event after Flask produces its response."""
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter

import requests
from dotenv import load_dotenv
from flask import Flask, current_app, g, request

load_dotenv(Path(__file__).with_name(".env"), interpolate=False)


def start_request_timer():
    g.request_started_at = perf_counter()


def record_request(response):
    if request.path == "/health":
        return response
    event = {
        "service": "general",
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration_ms": round((perf_counter() - getattr(g, "request_started_at", perf_counter())) * 1000, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    # stdout is useful for diagnosis but DOES NOT confirm storage in monitor DB.
    print(json.dumps(event, ensure_ascii=False), flush=True)
    token = os.getenv("EVENT_TOKEN", "")
    if not token:
        current_app.logger.warning("EVENT_TOKEN not set; HTTP event not sent")
        return response
    try:
        received = requests.post(
            os.getenv("MONITOR_URL", "http://127.0.0.1:5200/api/events"),
            json=event,
            headers={"X-Event-Token": token},
            timeout=(3, 10),
        )
        received.raise_for_status()
    except requests.RequestException:
        current_app.logger.warning("Monitor event delivery failed; check MONITOR_URL, EVENT_TOKEN and monitor logs")
    return response


def register_request_logging(app: Flask):
    """Compatibility wrapper for older lessons/tests."""
    app.before_request(start_request_timer)
    app.after_request(record_request)
