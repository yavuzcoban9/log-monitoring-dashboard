# send_log.py
import requests
from datetime import datetime, timezone  # <- en üste, importlar kısmına

URL = "http://127.0.0.1:8000/ingest"

payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(),  # <- artık timezone-aware
    "source": "test-client",
    "level": "INFO",
    "message": "Sistem düzgün çalışıyor.",
    "extra": {"user": "Yavuz", "module": "auth"}
}

response = requests.post(URL, json=payload, timeout=3)
print(response.status_code, response.text)
