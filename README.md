#  Log Monitoring & Alert Dashboard

A real-time **Log Monitoring Dashboard** built with **FastAPI**, **SQLite**, and **Chart.js**.  
This project collects, stores, and visualizes system logs, automatically detecting error spikes and sending alert notifications via **email (SMTP/Mailtrap)**.

---

## 🚀 Features

✅ **FastAPI Backend**
- RESTful API for log collection, search, and real-time access  
- SQLite database for local log storage  

✅ **Interactive Web Dashboard**
- Built with pure HTML, CSS, and Chart.js  
- Displays:
  - Bar chart (Log Level Distribution)
  - Line chart (Log Count over Time)
  - Pie chart (Log Level Ratios)
- Supports:
  - Live refresh every 10 seconds  
  - Light/Dark mode  
  - Pagination  
  - Filters by log level (INFO / WARNING / ERROR)

✅ **Alert System**
- Detects ≥3 ERROR logs within 60 seconds  
- Shows alert banner on dashboard  
- Sends **email alert** (via Mailtrap or Gmail SMTP)

##  Setup Instructions

###  Clone the repository
```bash
git clone https://github.com/yavuzcoban9/log-monitoring-dashboard.git
cd log-monitoring-dashboard


python -m venv venv
venv\Scripts\activate    # (Windows)

pip install -r requirements.txt

uvicorn app:app --reload --port 8000

Then open the dashboard:
 http://127.0.0.1:8000/dashboard

Email Alert Setup (Mailtrap)

Create a free account at Mailtrap.io


Copy SMTP credentials from “Email Testing → Inboxes → SMTP Settings”.

Edit your send_email.py file:

SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
USERNAME = "0f6f3862f02331"
EMAIL_PASSWORD = "YOUR_MAILTRAP_PASSWORD"


When ≥3 ERROR logs appear in 60 seconds, an alert banner appears and a test email is sent to Mailtrap inbox.

Example API Usage

Send a log:

curl -X POST "http://127.0.0.1:8000/ingest" \
     -H "Content-Type: application/json" \
     -d '{"source":"webapp","level":"ERROR","message":"Sample error detected"}'


Search logs:

curl "http://127.0.0.1:8000/search?q=error"


Author

Yavuz COBAN
Cybersecurity Enthusiast | Python & FastAPI Developer

 GitHub: https://github.com/yavuzcoban9
