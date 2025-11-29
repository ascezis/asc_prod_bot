import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Чтобы Python видел верхний уровень проекта
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Импорты из твоей структуры проекта
from app.database.connection import get_db_connection
from admin.backend.routers import admin_router

app = FastAPI(title="ASC Prod Bot API")

# CORS
origins = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
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

# Подключаем роутер без префикса (чтобы фронтенд мог обращаться к /clients и /projects)
app.include_router(admin_router)
