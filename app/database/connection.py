import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import config  # твой файл с настройками БД

logger = logging.getLogger(__name__)

# Создаем асинхронный engine
engine = create_async_engine(
    f"postgresql+asyncpg://{config.database.user}:{config.database.password}"
    f"@{config.database.host}:{config.database.port}/{config.database.name}",
    echo=True,  # логирование SQL-запросов
    future=True
)

# Фабрика асинхронных сессий
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Алиас для совместимости со старым кодом бота
AsyncSessionLocal = async_session

async def get_db_connection() -> AsyncSession:
    """
    Dependency для FastAPI.
    Используется в Depends для получения сессии.
    """
    async with async_session() as session:
        yield session

async def init_db():
    """Инициализация базы данных"""
    try:
        # Импортируем Base и все модели, чтобы они зарегистрировались в metadata
        from app.database.models import (
            Base,
            User,  # Важно: импортируем модели, чтобы они были в metadata
            Client,
            Project,
            AIAnalysis
        )

        async with engine.begin() as conn:
            # Создаем все таблицы
            await conn.run_sync(Base.metadata.create_all)

        logger.info("✅ База данных инициализирована успешно")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        return False
