import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import config
from app.bot.handlers.start import router as start_router
from app.bot.handlers.qualification import router as qualification_router
from app.bot.handlers.technical import router as technical_router
from app.bot.handlers.final import router as final_router
from app.bot.handlers.webapp import router as webapp_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🚀 Бот запускается...")
    
    # Используем MemoryStorage вместо Redis
    storage = MemoryStorage()
    
    bot = Bot(token=config.bot.token)
    dp = Dispatcher(storage=storage)
    
    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(webapp_router)  # Web App должен быть раньше, чтобы перехватывать web_app_data
    dp.include_router(qualification_router)
    dp.include_router(technical_router)
    dp.include_router(final_router)
    
    logger.info("✅ Бот запущен и готов к работе")
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
