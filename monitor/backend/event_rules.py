"""Classify original general-service HTTP responses before saving to PostgreSQL."""


def classify_event(method: str, path: str, status_code: int) -> str:
    if path in ("/api/auth/login", "/login", "/auth/login"):
        if status_code == 401:
            return "login_failure"
        if status_code == 200:
            return "login_success"
    if method == "GET" and path == "/" and status_code == 200:
        return "post_list"
    if status_code == 404:
        return "request_error"
    return "http_request"


def make_event(payload):
    if not isinstance(payload, dict):
        return None
    method = payload.get("method")
    path = payload.get("path")
    status = payload.get("status", payload.get("status_code"))
    if not isinstance(method, str) or not isinstance(path, str):
        return None
    method, path = method.strip().upper(), path.strip()
    if not method or not path or len(path) > 4096:
        return None
    try:
        status_code = int(status)
    except (ValueError, TypeError):
        return None
    if not 100 <= status_code <= 599:
        return None
    return {
        "service": "general",
        "method": method,
        "path": path,
        "status": status_code,
        "status_code": status_code,
        "event_type": classify_event(method, path, status_code),
        "duration_ms": payload.get("duration_ms"),
    }
