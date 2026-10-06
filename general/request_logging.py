import os
from datetime import datetime, timezone
from time import perf_counter

import requests
from flask import Flask, g, request


MONITOR_URL = os.getenv("MONITOR_URL", "http://127.0.0.1:5200/api/events")


def register_request_logging(app: Flask) -> None:
    @app.before_request
    def start_request_timer() -> None:
        g.request_started_at = perf_counter()

    @app.after_request
    def send_request_log(response):
        started_at = getattr(g, "request_started_at", perf_counter())
        payload = {
            "service": "general",
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round((perf_counter() - started_at) * 1000, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            requests.post(MONITOR_URL, json=payload, timeout=0.5)
        except requests.RequestException:
            app.logger.warning("감시 서비스에 요청 기록을 보내지 못했습니다.")

        return response
