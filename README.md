# ASC Prod Bot

Telegram-бот для приёма заявок на видеомонтаж с админ-панелью и AI-анализом заявок.

## Что делает

- Принимает заявки клиентов через Telegram и валидирует данные (длительность, ссылки, бюджет)
- Выполняет AI-анализ заявки через OpenRouter: реалистичность бюджета, сроки, риски, рекомендации
- Уведомляет администратора с результатами анализа
- Хранит клиентов, проекты и результаты анализа в PostgreSQL
- Предоставляет веб-админку для управления проектами

## Как это работает

1. Клиент отправляет заявку через Telegram.
2. Бот валидирует данные.
3. AI-анализ оценивает реалистичность, риски, стоимость и время.
4. Администратор получает уведомление с результатами.
5. Данные сохраняются в PostgreSQL.
6. Проектами можно управлять через админ-панель.

## Архитектура

| Компонент | Путь | Технологии |
|---|---|---|
| Telegram-бот | `app/` | Python, aiogram 3, SQLAlchemy, aiohttp |
| Backend админки | `admin/backend/` | FastAPI |
| Frontend админки | `admin/frontend/` | React, Vite |
| GUI-лаунчер | `admin-GUI/` | Electron |
| Менеджер процессов | `run.py` | запускает бот, API и фронтенд |

База данных: PostgreSQL. AI-анализ: OpenRouter (Claude, Grok, Gemini и др.).

Модели БД (`app/database/models.py`): `Client` (клиенты), `Project` (заявки), `AIAnalysis` (результаты анализа).

## Требования

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Telegram Bot Token
- OpenRouter API Key (для AI-анализа)

## Быстрый старт

### 1. Зависимости

```bash
# Виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
pip install -r admin/backend/requirements.txt

cd admin/frontend && npm install && cd ../..
```

Для Electron-лаунчера (по желанию): `cd admin-GUI && npm install`.

### 2. Конфигурация

Создайте файл `.env` в корне проекта:

```env
# Telegram
BOT_TOKEN=your_bot_token
BOT_ADMIN_ID=your_telegram_user_id

# База данных
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=video_editor_bot

# OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
```

Либо скопируйте `app/config.example.py` в `app/config.py` и заполните значения.

### 3. База данных

```bash
createdb video_editor_bot
```

Таблицы создаются автоматически при первом запуске. Вручную:
`python -m app.database.connection`.

### 4. Запуск

Все компоненты сразу:

```bash
python run.py
```

Запустятся Backend API (`http://localhost:8000`), Frontend (`http://localhost:5173`) и Telegram-бот. Остановка: `Ctrl+C`.

Другие варианты:

```bash
# Только бот
python -m app.main

# Только backend
cd admin/backend
uvicorn main:app --reload --port 8000

# Только frontend
cd admin/frontend
npm run dev
```

Windows: `start.bat` запускает только бота. Для запуска через окно с кнопками Start/Stop и логами: `cd admin-GUI && npm start`.

## API

Документация (Swagger): `http://localhost:8000/docs`

| Метод | Путь | Описание |
|---|---|---|
| GET | `/clients` | список клиентов |
| GET | `/projects` | список проектов |
| GET | `/projects/{id}` | детали проекта |
| POST | `/projects` | создание проекта |
| PUT | `/projects/{id}` | обновление проекта |
| DELETE | `/projects/{id}` | удаление проекта |

## Структура проекта

```
asc_prod_bot/
├── app/                    # Telegram-бот
│   ├── bot/                # обработчики, состояния, клавиатуры
│   ├── database/           # модели SQLAlchemy и подключение к БД
│   ├── services/           # AI-клиент, уведомления, валидация
│   ├── config.example.py   # пример конфигурации
│   └── main.py             # точка входа бота
├── admin/
│   ├── backend/            # FastAPI: routers/, main.py
│   └── frontend/           # React + Vite
├── admin-GUI/              # Electron-лаунчер
├── docs/                   # дополнительная документация
├── scripts/                # вспомогательные скрипты
├── run.py                  # менеджер процессов
└── requirements.txt
```

## Разработка

- Новый обработчик бота: создайте файл в `app/bot/handlers/` и зарегистрируйте роутер в `app/main.py`.
- Новый эндпоинт API: создайте роутер в `admin/backend/routers/` и подключите в `admin/backend/main.py`.

## Частые проблемы

- **Ошибка подключения к БД:** проверьте, что PostgreSQL запущен, база создана и настройки в `.env` верны.
- **Ошибка импорта модулей:** активируйте виртуальное окружение и выполните `pip install -r requirements.txt`.
- **Frontend не запускается:** проверьте `node --version` и выполните `npm install` в `admin/frontend`.
- **Бот не отвечает:** проверьте `BOT_TOKEN` и логи запуска.

## Безопасность

- Не храните токены, пароли и ключи в репозитории: `.env` и `app/config.py` должны быть в `.gitignore`.
- API-ключи и токен бота должны оставаться приватными.

## Лицензия

ISC