import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def redact_request(event, hint):
    request_data = event.get("request", {})
    for key in ("data", "cookies", "headers", "query_string"):
        request_data.pop(key, None)
    event.pop("user", None)
    return event


def configure_errors(service_name: str):
    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        return
    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        environment=os.getenv("SENTRY_ENVIRONMENT", service_name),
        release=os.getenv("APP_VERSION", "day2-v1"),
        send_default_pii=False,
        include_local_variables=False,
        max_request_body_size="never",
        traces_sample_rate=0.0,
        before_send=redact_request,
    )
    sentry_sdk.set_tag("service", service_name)
