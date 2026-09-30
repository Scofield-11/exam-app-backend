from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import exam
import os


app = FastAPI(title="Exam App API")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "")
if CORS_ORIGINS:
    origins = [origin.strip() for origin in CORS_ORIGINS.split(",")]
else:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exam.router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Exam App Backend is running properly!"}
    return {"status": "ok", "message": "Backend API is running properly on Render!"}

# --- CHỐNG SLEEP CHO RENDER (Tự động Ping mỗi 9 phút) ---
import threading
import time
import urllib.request

def keep_alive_ping():
    # Render tự động cấp biến môi trường RENDER_EXTERNAL_URL khi deploy
    url = os.getenv("RENDER_EXTERNAL_URL") or "https://scofield-backend.onrender.com/"
    if not url.endswith("/"):
        url += "/"

    while True:
        time.sleep(9 * 60)  # Ping mỗi 9 phút để đảm bảo không chạm mốc 15 phút của Render
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Render-KeepAlive/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                print(f"Self-ping status {response.getcode()} to keep Render awake.")
        except Exception as e:
            print(f"Self-ping failed: {e}")

# Chỉ chạy ping ngầm khi đang trên môi trường production của Render
if os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_URL"):
    threading.Thread(target=keep_alive_ping, daemon=True).start()