import sys
import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from admin.backend.routers import projects, clients, statistics
from app.database.connection import init_db
# Чтобы Python видел верхний уровень проекта
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = FastAPI(title="ASC Prod Bot API")

# Инициализация БД при старте
@app.on_event("startup")
async def startup_event():
    """Инициализация базы данных при запуске приложения"""
    try:
        await init_db()
        print("[OK] База данных инициализирована")
    except Exception as e:
        print(f"[ERROR] Ошибка инициализации БД: {e}")

# CORS - разрешаем все локальные порты для разработки
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Подключаем роутеры
app.include_router(clients.router)
app.include_router(projects.router)
app.include_router(statistics.router)
