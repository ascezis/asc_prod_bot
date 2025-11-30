# Настройка .env файла

## Где находится .env файл?

Файл `.env` должен находиться в **корне проекта** (там же, где `run.py`).

## Как создать .env файл?

1. Создайте файл `.env` в корне проекта (рядом с `run.py`)
2. Скопируйте содержимое из этого файла и заполните своими значениями:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
BOT_ADMIN_ID=7229606042

# Database Configuration
DB_USER=video_user
DB_PASSWORD=ascezis_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=video_editor_bot

# OpenRouter AI Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
```

## Важно!

- Файл `.env` находится в `.gitignore`, поэтому он не будет закоммичен в репозиторий
- После создания `.env` файла перезапустите приложение
- Убедитесь, что все значения заполнены правильно

