"""Pure functions. All results and evidence derive from the SAME selected rows."""
from datetime import datetime, timezone


def _received_at(event):
    value = event["received_at"]
    instant = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else value
    if instant.tzinfo is None:
        raise ValueError("Received timestamps must include a timezone")
    return instant.astimezone(timezone.utc)


def select_views(events):
    return [
        row for row in events
        if row["method"] == "GET"
        and row["path"] == "/"
        and row["status_code"] == 200
        and row["kind"] == "post_list"
    ]


def find_following_errors(events, views):
    if not views:
        return []
    last_view_at = max(_received_at(view) for view in views)
    return [
        row for row in events
        if row["status_code"] == 404
        and 0 < (_received_at(row) - last_view_at).total_seconds() <= 30
    ]


def evaluate(views, threshold):
    if type(threshold) is not int or threshold < 1:
        raise ValueError("Threshold must be a positive integer")
    return len(views) >= threshold
