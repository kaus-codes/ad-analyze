# Mobile ad dashbord (event based)

A Python-based mobile advertising event validation and QA analytics project built using FastAPI, SQLite, SQL, Tableau, and Pytest.

The project simulates mobile advertising events from Android and iOS clients, reproduces an event-schema mismatch, investigates its impact using SQL, implements a backend fix, and compares pre-fix and post-fix results through a Tableau dashboard.

**Note:** All mobile clients, advertisers, campaigns, and advertising events in this project are synthetic and created for demonstration purposes.

## Project Overview

The project simulates a mobile advertising backend that receives three types of events:

- Impressions
- Clicks
- Conversions

A simulated issue occurs when Android application version 2.0 submits `purchase` instead of the expected `conversion` event name.

The backend initially rejects these requests. SQL queries are used to investigate the failures, identify affected advertisers, and isolate the problematic application version.

A backend normalization fix maps `purchase` to `conversion`, after which the same dataset is replayed to verify the resolution.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and backend logic |
| FastAPI | REST API and event validation |
| SQLite | Event logging and storage |
| SQL | Root-cause analysis |
| Tableau | QA analytics dashboard |
| Pytest | Automated regression testing |
| Jira | Bug tracking and documentation |

## Project Structure

```text
mobile-ad-event-qa-dashboard/
│
├── app/
│   ├── main.py
│   ├── database.py
│   └── event_validator.py
│
├── scripts/
│   ├── generate_events.py
│   ├── simulate_requests.py
│   └── export_dashboard_data.py
│
├── sql/
│   └── investigation_queries.sql
│
├── tests/
│   └── test_events.py
│
├── data/
│   ├── events.csv
│   └── events.db
│
├── dashboard/
│   └── screenshots/
│
├── docs/
│   └── incident_report.md
│
├── requirements.txt
└── README.md
```

## Prerequisites

Install the following:

- Python 3.10 or later
- pip
- Tableau Desktop or Tableau Public
- Git (optional)

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/mobile-ad-event-qa-dashboard.git
```

Navigate into the project:

```bash
cd mobile-ad-event-qa-dashboard
```

Create a virtual environment:

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure the following directories exist:

```bash
mkdir data
mkdir dashboard
mkdir dashboard/screenshots
```

## Running the Project

### Step 1: Generate Synthetic Events

Generate 5,000 synthetic advertising events:

```bash
python scripts/generate_events.py
```

The generated dataset includes:

- 5,000 advertising event requests
- 20 simulated advertisers
- 60 simulated campaigns
- Android and iOS platforms
- Application versions 1.9 and 2.0
- Impressions, clicks, and conversions

The dataset uses a fixed random seed to ensure reproducibility.

### Step 2: Start the FastAPI Server

Run:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Step 3: Reproduce the Bug

Open a second terminal and activate the virtual environment.

Run:

```bash
python scripts/simulate_requests.py before_fix
```

This sends all 5,000 generated requests to the API.

The backend initially expects `conversion`, while Android 2.0 sends `purchase`.

The affected requests are rejected and recorded in SQLite.

### Step 4: Apply the Fix

Stop the FastAPI server.

Enable event normalization.

**Windows PowerShell:**

```powershell
$env:PURCHASE_ALIAS_ENABLED="true"
uvicorn app.main:app --reload
```

**macOS/Linux:**

```bash
PURCHASE_ALIAS_ENABLED=true uvicorn app.main:app --reload
```

The backend now maps:

```text
purchase → conversion
```

### Step 5: Replay the Same Dataset

Open another terminal and run:

```bash
python scripts/simulate_requests.py after_fix
```

The same 5,000 requests are replayed with a different run identifier.

Both runs are stored in SQLite, allowing direct before-and-after comparisons.

## SQL Investigation

The project uses SQL to investigate four questions:

1. What percentage of events were rejected in each run?
2. Which platform and application version experienced the most failures?
3. How many simulated advertisers were affected?
4. Did valid event types continue working after the fix?

The investigation queries are available in:

```text
sql/investigation_queries.sql
```

## Automated Testing

Run the regression tests:

```bash
pytest -v
```

The tests verify:

1. Valid conversion events are accepted.
2. Purchase events are normalized and accepted after the fix.
3. Unsupported event names are still rejected.

## Tableau Dashboard

Export the event logs:

```bash
python scripts/export_dashboard_data.py
```

This generates:

```text
data/dashboard_events.csv
```

Connect the CSV file to Tableau.

The dashboard includes:

- Total requests
- Event rejection rate
- Number of affected advertisers
- Rejection rate by platform and application version
- Before-and-after rejection counts

Dashboard screenshots are available in:

```text
dashboard/screenshots/
```

All dashboard metrics should be calculated from the actual SQLite event logs rather than manually entered values.

## Bug Summary

**Issue:** Android 2.0 conversion events rejected by backend validation.

**Root Cause:** The mobile client submitted `purchase` while the backend expected `conversion`.

**Resolution:** Implemented event-name normalization to map `purchase` to `conversion` before validation.

**Verification:** Replayed the original synthetic dataset and executed automated regression tests to verify the fix.

## Documentation and Issue Tracking

The project uses Jira-style issue tracking to document:

- API development
- Bug reproduction
- Root-cause investigation
- Backend fix implementation
- Regression testing and verification

The incident report is available in:

```text
docs/incident_report.md
```

## Project Goals

This project demonstrates practical experience with:

- REST API development
- Python backend engineering
- SQL-based data investigation
- Mobile-client troubleshooting simulation
- Root-cause analysis
- Regression testing
- Data visualization
- Defect documentation and tracking

---

**Disclaimer:** This is an independent portfolio project using synthetic advertising data. It does not integrate with real advertising networks or production mobile applications.