
import pandas as pd
from app.database import get_connection

conn = get_connection()

df = pd.read_sql_query(
    "SELECT * FROM event_logs",
    conn
)

df.to_csv(
    "data/dashboard_events.csv",
    index=False
)

conn.close()

print("Dashboard data exported successfully.")
