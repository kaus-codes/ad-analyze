
import os
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from app.database import get_connection, init_db
from app.event_validator import validate_event

app = FastAPI(title="Mobile Ad Event QA API")

APPLY_FIX = os.getenv("PURCHASE_ALIAS_ENABLED", "false").lower() == "true"


class AdEvent(BaseModel):
    run_id: str
    request_id: str
    advertiser_id: str
    campaign_id: str
    platform: str
    app_version: str
    event_name: str


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/events")
def receive_event(event: AdEvent):
    accepted, normalized, error = validate_event(
        event.event_name,
        apply_fix=APPLY_FIX
    )

    conn = get_connection()

    conn.execute("""
        INSERT INTO event_logs (
            run_id, request_id, advertiser_id,
            campaign_id, platform, app_version,
            event_name, normalized_event,
            accepted, error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.run_id,
        event.request_id,
        event.advertiser_id,
        event.campaign_id,
        event.platform,
        event.app_version,
        event.event_name,
        normalized,
        int(accepted),
        error
    ))

    conn.commit()
    conn.close()

    return {
        "request_id": event.request_id,
        "accepted": accepted,
        "normalized_event": normalized,
        "error": error
    }
