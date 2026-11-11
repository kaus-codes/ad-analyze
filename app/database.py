
import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "data/events.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS event_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            advertiser_id TEXT NOT NULL,
            campaign_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            app_version TEXT NOT NULL,
            event_name TEXT NOT NULL,
            normalized_event TEXT,
            accepted INTEGER NOT NULL,
            error_message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_run_id
        ON event_logs(run_id)
    """)

    conn.commit()
    conn.close()

