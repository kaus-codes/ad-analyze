
import csv
import random
import uuid

random.seed(42)

EVENTS = ["impression", "click", "conversion"]
PLATFORMS = ["Android", "iOS"]
VERSIONS = ["1.9", "2.0"]

with open("data/events.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "request_id", "advertiser_id",
            "campaign_id", "platform",
            "app_version", "event_name"
        ]
    )

    writer.writeheader()

    for i in range(5000):
        platform = random.choice(PLATFORMS)
        version = random.choice(VERSIONS)
        event = random.choices(
            EVENTS,
            weights=[40, 35, 25]
        )[0]

        # Simulated mobile-client bug
        if (
            platform == "Android"
            and version == "2.0"
            and event == "conversion"
        ):
            event = "purchase"

        writer.writerow({
            "request_id": str(uuid.uuid4()),
            "advertiser_id": f"ADV-{random.randint(1, 20):03}",
            "campaign_id": f"CAMP-{random.randint(1, 60):03}",
            "platform": platform,
            "app_version": version,
            "event_name": event
        })

print("Generated 5,000 simulated advertising events.")
