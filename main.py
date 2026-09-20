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
    return {"status": "ok", "message": "Backend API is running properly on Render!"}

# --- CHỐNG SLEEP CHO RENDER (Tự động Ping mỗi 14 phút) ---
import threading
import time
import urllib.request

def keep_alive_ping():
    url = "https://scofield-backend.onrender.com/"
    while True:
        time.sleep(14 * 60) # Chờ 14 phút (Render sleep sau 15 phút)
        try:
            urllib.request.urlopen(url, timeout=10)
            print("Self-ping successful to keep Render awake.")
        except Exception as e:
            print(f"Self-ping failed: {e}")

# Chạy ngầm một luồng (thread) ping tự động khi server khởi động
threading.Thread(target=keep_alive_ping, daemon=True).start()