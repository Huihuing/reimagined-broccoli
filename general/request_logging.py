import os
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter
import requests
from dotenv import load_dotenv
from flask import Flask, g, request

load_dotenv(Path(__file__).with_name(".env"), interpolate=False)


def register_request_logging(app: Flask) -> None:
    @app.before_request
    def start_request_timer() -> None:
        g.request_started_at = perf_counter()

    @app.after_request
    def send_request_log(response):
        if request.path == "/health":
            return response
        payload = {
            "service": "general",
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round((perf_counter() - getattr(g, "request_started_at", perf_counter())) * 1000, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        token = os.getenv("EVENT_TOKEN", "")
        if not token:
            app.logger.warning("EVENT_TOKEN 미설정: 요청 기록 전송 생략")
            return response
        try:
            result = requests.post(
                os.getenv("MONITOR_URL", "http://127.0.0.1:5200/api/events"),
                json=payload, headers={"X-Event-Token": token},
                timeout=(3, 10),
            )
            result.raise_for_status()
        except requests.RequestException:
            app.logger.warning("감시 전송 실패: MONITOR_URL, EVENT_TOKEN 및 /health 확인")
        return response
