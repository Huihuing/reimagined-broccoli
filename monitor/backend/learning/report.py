"""One HTTP detection-review card from real normalized DB rows."""
from learning.normalize import normalize_events
from learning.http_rules import select_views, find_following_errors, evaluate


def build_report(original_rows, threshold: int, after_id: int, reference_time):
    normalized = normalize_events(original_rows)
    views = select_views(normalized)
    following = find_following_errors(normalized, views)
    supporting = sorted([*views, *following], key=lambda row: row["original_id"])
    observed = len(views)
    match = evaluate(views, threshold)
    return {
        "ready": True,
        "after_id": after_id,
        "reference_time": reference_time.isoformat() if hasattr(reference_time, "isoformat") else str(reference_time),
        "card": {
            "rule": "HTTP 게시판 목록 조회 빈도",
            "observed": observed,
            "threshold": threshold,
            "matched": match,
            "verdict": "검토 후보" if match else "기준 미해당",
            "reason": (
                f"조회 {observed}회가 기준 {threshold}회 이상입니다. "
                if match else f"조회 {observed}회는 기준 {threshold}회 미만입니다. "
            ) + f"뒤따른 404 {len(following)}행은 문맥 근거일 뿐 조회 횟수에서 제외했습니다.",
            "view_ids": [row["id"] for row in views],
            "following_error_ids": [row["id"] for row in following],
            "evidence": [row["id"] for row in supporting],
            "records": supporting,
            "view_count": observed,
            "following_error_count": len(following),
        },
    }
