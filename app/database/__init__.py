# app/database/init_db.py
import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, ForeignKey, ARRAY
from sqlalchemy.sql import func

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

Base = declarative_base()

# ------------------------------
# Модели
# ------------------------------
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)  # BIGINT для больших Telegram ID
    username = Column(String(100))
    full_name = Column(String(200))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    project_type = Column(String(50))
    duration_raw = Column(String(50))
    duration_final = Column(String(50))
    services = Column(ARRAY(String))
    deadline = Column(String(50))
    budget = Column(String(50))
    source_links = Column(String)
    style_examples = Column(String)
    additional_notes = Column(String)
    status = Column(String(20), default="new")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    realism_score = Column(Integer)
    recommended_price = Column(Integer)
    time_estimate = Column(Integer)
    risks_detected = Column(ARRAY(String))
    used_model = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

# ------------------------------
# Функция инициализации БД
# ------------------------------
async def init_db():
    """
    Создаёт все таблицы заново.
    ⚠️ Drop_all удаляет старые таблицы!
    """
    from app.config import config

    DATABASE_URL = (
        f"postgresql+asyncpg://{config.database.user}:"
        f"{config.database.password}@{config.database.host}:"
        f"{config.database.port}/{config.database.name}"
    )

    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        logger.info("🚀 Создание таблиц в БД...")
        await conn.run_sync(Base.metadata.drop_all)    # удаляет старые таблицы
        await conn.run_sync(Base.metadata.create_all)  # создаёт новые таблицы
        logger.info("✅ Таблицы созданы")

    await engine.dispose()

# ------------------------------
# Запуск из командной строки
# ------------------------------
if __name__ == "__main__":
    asyncio.run(init_db())
