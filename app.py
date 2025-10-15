from fastapi import FastAPI, Query, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3, json, os
from fastapi.responses import FileResponse
from send_email import send_alert_email

app = FastAPI(title="Log Monitoring API")

# --- SQLite bağlantısı ---
conn = sqlite3.connect("logs.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT,
    source TEXT,
    level TEXT,
    message TEXT,
    raw TEXT
)
""")
conn.commit()

# --- Veri modeli ---
class LogItem(BaseModel):
    timestamp: Optional[str] = None
    source: str
    level: str
    message: str

# --- POST /ingest : Yeni log ekleme ---
@app.post("/ingest")
def ingest_log(item: LogItem):
    ts = item.timestamp or datetime.utcnow().isoformat() + "Z"
    raw_json = json.dumps(item.dict(), ensure_ascii=False)

    cur.execute(
        "INSERT INTO logs (ts, source, level, message, raw) VALUES (?, ?, ?, ?, ?)",
        (ts, item.source, item.level, item.message, raw_json),
    )
    conn.commit()

    return {"status": "ok", "inserted_ts": ts}

# --- GET /recent : Son eklenen logları getir ---
@app.get("/recent")
def get_recent(limit: int = 50):
    rows = cur.execute(
        "SELECT id, ts, source, level, message FROM logs ORDER BY id DESC LIMIT ?", 
        (limit,)
    ).fetchall()
    return [{"id": r[0], "ts": r[1], "source": r[2], "level": r[3], "message": r[4]} for r in rows]

# --- GET /search : Basit arama ---
@app.get("/search")
def search(q: Optional[str] = Query(None), level: Optional[str] = None, source: Optional[str] = None,
           from_ts: Optional[str] = None, to_ts: Optional[str] = None, limit: int = 100):
    sql = "SELECT id, ts, source, level, message FROM logs WHERE 1=1"
    params: List = []

    if q:
        sql += " AND (message LIKE ? OR source LIKE ? OR raw LIKE ?)"
        likeq = f"%{q}%"
        params.extend([likeq, likeq, likeq])
    if level:
        sql += " AND level = ?"
        params.append(level)
    if source:
        sql += " AND source = ?"
        params.append(source)
    if from_ts:
        sql += " AND ts >= ?"
        params.append(from_ts)
    if to_ts:
        sql += " AND ts <= ?"
        params.append(to_ts)

    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    rows = cur.execute(sql, params).fetchall()
    return [{"id": r[0], "ts": r[1], "source": r[2], "level": r[3], "message": r[4]} for r in rows]

# --- Basit ana sayfa ---
@app.get("/")
def index():
    return {"message": "Basit Log Toplayıcı. /ingest POST, /recent GET, /search?q=... kullanın. API dokümanı: /docs"}

# --- YENİ: Dashboard (HTML) ---
@app.get("/dashboard")
def get_dashboard():
    file_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    return FileResponse(file_path)

# --- YENİ: Uyarı e-postası gönderme ---
@app.post("/send-alert")
def send_alert(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(send_alert_email, message)
    return {"status": "ok", "detail": "Email gönderiliyor"}
