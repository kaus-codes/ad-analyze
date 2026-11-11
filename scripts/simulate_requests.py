
import csv
import sys
import requests

RUN_ID = sys.argv[1]

API_URL = "http://127.0.0.1:8000/events"

with open("data/events.csv") as file:
    events = csv.DictReader(file)

    for event in events:
        payload = {
            **event,
            "run_id": RUN_ID
        }

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            print("Unexpected API error:", response.text)

print(f"Finished processing run: {RUN_ID}")
