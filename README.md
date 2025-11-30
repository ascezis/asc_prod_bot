# ASC Prod Bot

Telegram-бот для приема заявок на видеомонтаж с админ-панелью и AI-анализом заявок.

## 🏗️ Архитектура

Проект состоит из трех компонентов:
- **Telegram Bot** (`app/`) - прием заявок от клиентов
- **Admin Backend** (`admin/backend/`) - FastAPI REST API
- **Admin Frontend** (`admin/frontend/`) - React админ-панель

## 📋 Требования

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Telegram Bot Token
- OpenRouter API Key (для AI-анализа)
- Electron (устанавливается автоматически через npm)

## 🚀 Быстрый старт

### 1. Клонирование и настройка окружения

```bash
# Активация виртуального окружения (если есть)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка Python зависимостей
pip install -r requirements.txt
pip install -r admin/backend/requirements.txt
```

### 2. Настройка конфигурации

Создайте файл `.env` в корне проекта (или скопируйте из `app/config.example.py`):

```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
BOT_ADMIN_ID=your_telegram_user_id

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

**Или** создайте файл `app/config.py` на основе `app/config.example.py` и заполните значениями.

### 3. Настройка базы данных

```bash
# Создайте базу данных PostgreSQL
createdb video_editor_bot

# Или через psql:
psql -U postgres
CREATE DATABASE video_editor_bot;
CREATE USER video_user WITH PASSWORD 'ascezis_pass';
GRANT ALL PRIVILEGES ON DATABASE video_editor_bot TO video_user;
\q
```

Инициализация таблиц (опционально, таблицы создадутся автоматически при первом запуске):
```bash
python -m app.database.connection
```

### 4. Установка Frontend зависимостей

**Для React админ-панели:**
```bash
cd admin/frontend
npm install
cd ../..
```

**Для Electron GUI (опционально, но рекомендуется):**
```bash
cd admin-GUI
npm install
cd ..
```

### 5. Запуск проекта

#### Вариант 1: Запуск через Electron GUI (рекомендуется для Windows)

```bash
cd admin-GUI
npm install
npm start
```

Откроется окно Electron с кнопками управления. Нажмите "Start" для запуска всех компонентов:
- Backend API на `http://localhost:8000`
- Frontend на `http://localhost:5173`
- Telegram Bot

Логи будут отображаться в окне Electron. Для остановки нажмите "Stop".

#### Вариант 2: Запуск всех компонентов через менеджер процессов

```bash
python run.py
```

Это запустит:
- Backend API на `http://localhost:8000`
- Frontend на `http://localhost:5173` (или другой порт Vite)
- Telegram Bot

Для остановки нажмите `Ctrl+C`.

#### Вариант 3: Запуск компонентов отдельно

**Backend API:**
```bash
cd admin/backend
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd admin/frontend
npm run dev
```

**Telegram Bot:**
```bash
python -m app.main
```

#### Вариант 4: Только бот (Windows)

```bash
start.bat
```

## 📁 Структура проекта

```
asc_prod_bot/
├── app/                    # Telegram бот
│   ├── bot/               # Обработчики бота
│   ├── database/          # Модели и подключение к БД
│   ├── services/          # AI клиент, уведомления
│   ├── config.py          # Конфигурация (создать!)
│   └── main.py            # Точка входа бота
├── admin/
│   ├── backend/           # FastAPI backend
│   │   ├── routers/       # API роуты
│   │   ├── models.py      # Реэкспорт моделей
│   │   └── main.py        # FastAPI приложение
│   └── frontend/          # React админ-панель
│       └── src/
├── run.py                 # Менеджер процессов
└── requirements.txt       # Python зависимости
```

## 🔧 Настройка

### Конфигурация бота

Все настройки находятся в `app/config.py` или загружаются из `.env` файла.

### База данных

Модели БД находятся в `app/database/models.py`:
- `Client` - клиенты бота
- `Project` - заявки на проекты
- `AIAnalysis` - результаты AI-анализа

### API Endpoints

- `GET /clients` - список клиентов
- `GET /projects` - список проектов
- `GET /projects/{id}` - детали проекта
- `POST /projects` - создание проекта
- `PUT /projects/{id}` - обновление проекта
- `DELETE /projects/{id}` - удаление проекта

API документация доступна по адресу: `http://localhost:8000/docs`

## 🐛 Решение проблем

### Ошибка подключения к БД
- Проверьте, что PostgreSQL запущен
- Проверьте настройки в `config.py` или `.env`
- Убедитесь, что база данных создана

### Ошибка импорта модулей
- Убедитесь, что виртуальное окружение активировано
- Проверьте, что все зависимости установлены: `pip install -r requirements.txt`

### Frontend не запускается
- Убедитесь, что Node.js установлен: `node --version`
- Установите зависимости: `cd admin/frontend && npm install`

### Бот не отвечает
- Проверьте `BOT_TOKEN` в конфигурации
- Убедитесь, что бот запущен: проверьте логи

## 📝 Разработка

### Добавление новых обработчиков бота

Создайте файл в `app/bot/handlers/` и зарегистрируйте роутер в `app/main.py`.

### Добавление новых API endpoints

Создайте роутер в `admin/backend/routers/` и подключите в `admin/backend/main.py`.

## 📄 Лицензия

ISC

