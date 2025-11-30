"""
Пример конфигурационного файла
Скопируйте этот файл в app/config.py и заполните своими значениями
Или используйте .env файл с переменными окружения
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()


@dataclass
class BotConfig:
    """Конфигурация Telegram бота"""
    token: str = os.getenv("BOT_TOKEN", "your_bot_token_here")
    admin_id: int = int(os.getenv("BOT_ADMIN_ID", "0"))


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    user: str = os.getenv("DB_USER", "video_user")
    password: str = os.getenv("DB_PASSWORD", "ascezis_pass")
    host: str = os.getenv("DB_HOST", "localhost")
    port: str = os.getenv("DB_PORT", "5432")
    name: str = os.getenv("DB_NAME", "video_editor_bot")


@dataclass
class AIConfig:
    """Конфигурация AI сервиса (OpenRouter)"""
    api_key: str = os.getenv("OPENROUTER_API_KEY", "your_openrouter_api_key_here")
    base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")


@dataclass
class Config:
    """Главный класс конфигурации"""
    bot: BotConfig = field(default_factory=BotConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    ai: AIConfig = field(default_factory=AIConfig)


# Создаем глобальный экземпляр конфигурации
config = Config()

