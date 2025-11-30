# 🚀 Полная инструкция по запуску проекта

## 📋 Содержание
1. [Подготовка окружения](#подготовка-окружения)
2. [Настройка базы данных](#настройка-базы-данных)
3. [Настройка конфигурации](#настройка-конфигурации)
4. [Установка зависимостей](#установка-зависимостей)
5. [Создание первого пользователя](#создание-первого-пользователя)
6. [Запуск проекта](#запуск-проекта)
7. [Настройка Web App (опционально)](#настройка-web-app)
8. [Проверка работоспособности](#проверка-работоспособности)

---

## 🔧 Подготовка окружения

### 1. Проверьте установленные программы

```bash
# Python (должен быть 3.10+)
python --version

# Node.js (должен быть 18+)
node --version

# PostgreSQL (должен быть 14+)
psql --version
```

### 2. Активируйте виртуальное окружение

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Если виртуального окружения нет, создайте его:
```bash
python -m venv venv
```

---

## 🗄️ Настройка базы данных

### 1. Создайте базу данных PostgreSQL

```bash
# Войдите в PostgreSQL
psql -U postgres

# Выполните команды:
CREATE DATABASE video_editor_bot;
CREATE USER video_user WITH PASSWORD 'ascezis_pass';
GRANT ALL PRIVILEGES ON DATABASE video_editor_bot TO video_user;
\q
```

### 2. Проверьте подключение

```bash
psql -U video_user -d video_editor_bot -h localhost
```

Если подключение успешно, выйдите: `\q`

---

## ⚙️ Настройка конфигурации

### 1. Создайте файл конфигурации

Скопируйте пример конфигурации:
```bash
copy app\config.example.py app\config.py
```

**Или вручную создайте `app/config.py`** на основе `app/config.example.py`

### 2. Заполните обязательные параметры

Откройте `app/config.py` и укажите:

```python
@dataclass
class BotConfig:
    token: str = "ВАШ_TELEGRAM_BOT_TOKEN"  # Получите у @BotFather
    admin_id: int = 7229606042  # Ваш Telegram ID

@dataclass
class DatabaseConfig:
    user: str = "video_user"
    password: str = "ascezis_pass"
    host: str = "localhost"
    port: int = 5432
    name: str = "video_editor_bot"

@dataclass
class AIConfig:
    api_key: str = "ВАШ_OPENROUTER_API_KEY"  # Получите на openrouter.ai
    base_url: str = "https://openrouter.ai/api/v1/chat/completions"
```

### 3. Настройте JWT Secret Key (для админ-панели)

Создайте файл `.env` в корне проекта (опционально):

```env
JWT_SECRET_KEY=ваш-очень-секретный-ключ-минимум-32-символа
```

Или укажите в `admin/backend/auth.py` напрямую.

---

## 📦 Установка зависимостей

### 1. Python зависимости

```bash
# Основные зависимости
pip install -r requirements.txt

# Зависимости для backend
pip install -r admin/backend/requirements.txt
```

### 2. Frontend зависимости

```bash
# React админ-панель
cd admin/frontend
npm install
cd ../..
```

---

## 👤 Создание первого пользователя

### 1. Создайте пользователя-владельца (Owner)

```bash
python scripts/create_owner_simple.py
```

Введите:
- **Username** - имя пользователя
- **Email** - email адрес
- **Password** - пароль

**Важно:** Запомните эти данные! Они понадобятся для входа в админ-панель.

### 2. (Опционально) Создайте других пользователей

```bash
python scripts/create_user.py
```

---

## 🚀 Запуск проекта

### Вариант 1: Запуск всех компонентов одновременно (рекомендуется)

```bash
python run.py
```

Это запустит:
- ✅ Backend API на `http://localhost:8000`
- ✅ Frontend на `http://localhost:5173`
- ✅ Telegram Bot

**Для остановки:** Нажмите `Ctrl+C`

### Вариант 2: Запуск компонентов отдельно

**Терминал 1 - Backend:**
```bash
python -m uvicorn admin.backend.main:app --reload --port 8000
```

**Терминал 2 - Frontend:**
```bash
cd admin/frontend
npm run dev
```

**Терминал 3 - Bot:**
```bash
python -m app.main
```

---

## 📱 Настройка Web App (опционально)

### 1. Запустите Web App сервер

```bash
python app/webapp/server.py
```

Сервер запустится на `http://localhost:8080`

### 2. Запустите ngrok для Web App

В новом терминале:
```bash
ngrok http 8080
```

Скопируйте HTTPS URL (например: `https://xxxx-xx-xx-xx-xx.ngrok-free.dev`)

### 3. Обновите URL в коде

**Способ 1: Автоматически (скрипт)**
```bash
python scripts/update_webapp_url.py https://ваш-ngrok-url.ngrok-free.dev
```

**Способ 2: Вручную**

В файлах `app/bot/handlers/start.py` и `app/bot/handlers/webapp.py` замените:
```python
web_app_url = "https://ваш-ngrok-url.ngrok-free.dev/index.html"
```

В файле `app/webapp/app.js` обновите `API_URL`:
```javascript
const API_URL = 'https://ваш-ngrok-url.ngrok-free.dev';
```

**Важно:** Если backend на отдельном порту, запустите второй ngrok:
```bash
ngrok http 8000
```

И укажите этот URL в `app/webapp/app.js` как `API_URL`.

### 4. Обновите CORS в backend

В `admin/backend/main.py` добавьте ваш ngrok домен в список `origins`:
```python
origins = [
    # ... существующие ...
    "https://ваш-ngrok-url.ngrok-free.dev",
]
```

---

## ✅ Проверка работоспособности

### 1. Backend работает?

Откройте в браузере: `http://localhost:8000/docs`

Должна открыться страница Swagger UI с документацией API.

### 2. Frontend работает?

Откройте в браузере: `http://localhost:5173`

Должна открыться админ-панель. Войдите с данными Owner пользователя.

### 3. Bot работает?

Откройте Telegram и найдите вашего бота. Отправьте `/start`.

Бот должен ответить и предложить создать заявку.

### 4. Web App работает?

1. Отправьте боту `/start`
2. Нажмите "📱 Создать через Web App"
3. Web App должен открыться в Telegram

---

## 🔍 Решение проблем

### Backend не запускается

**Проблема:** Ошибка подключения к БД
```bash
# Проверьте, что PostgreSQL запущен
# Windows: Проверьте службу PostgreSQL
# Linux: sudo systemctl status postgresql

# Проверьте настройки в app/config.py
```

**Проблема:** Порт 8000 занят
```bash
# Найдите процесс
netstat -ano | findstr :8000

# Или измените порт в run.py
```

### Frontend не запускается

**Проблема:** Ошибка зависимостей
```bash
cd admin/frontend
rm -rf node_modules
npm install
```

**Проблема:** Порт 5173 занят
```bash
# Vite автоматически выберет другой порт
# Или измените в vite.config.js
```

### Bot не отвечает

**Проблема:** Неверный токен
```bash
# Проверьте BOT_TOKEN в app/config.py
# Получите новый токен у @BotFather в Telegram
```

### Web App не открывается

**Проблема:** ERR_CONNECTION_REFUSED
```bash
# Убедитесь, что:
# 1. Web App сервер запущен (python app/webapp/server.py)
# 2. ngrok работает (ngrok http 8080)
# 3. URL в коде бота правильный
```

**Проблема:** CORS ошибки
```bash
# Проверьте, что ngrok домен добавлен в CORS в admin/backend/main.py
```

---

## 📝 Быстрая шпаргалка

```bash
# 1. Активация окружения
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Запуск всего проекта
python run.py

# 3. Или отдельно:
# Backend: python -m uvicorn admin.backend.main:app --reload --port 8000
# Frontend: cd admin/frontend && npm run dev
# Bot: python -m app.main
# Web App: python app/webapp/server.py

# 4. Проверка:
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
# Bot: /start в Telegram
```

---

## 🎯 Порядок запуска (кратко)

1. ✅ Активируйте виртуальное окружение
2. ✅ Убедитесь, что PostgreSQL запущен
3. ✅ Проверьте `app/config.py` (токены и настройки БД)
4. ✅ Запустите `python run.py`
5. ✅ Откройте `http://localhost:8000/docs` - проверьте Backend
6. ✅ Откройте `http://localhost:5173` - войдите в админ-панель
7. ✅ Отправьте `/start` боту - проверьте работу бота
8. ✅ (Опционально) Запустите Web App сервер и ngrok

---

## 🔐 Важные данные

**База данных:**
- Имя БД: `video_editor_bot`
- Пользователь: `video_user`
- Пароль: `ascezis_pass`
- Хост: `localhost`
- Порт: `5432`

**Порты:**
- Backend: `8000`
- Frontend: `5173` (или другой, если занят)
- Web App: `8080`
- PostgreSQL: `5432`

**Файлы конфигурации:**
- `app/config.py` - основная конфигурация (токены, БД, AI)
- `.env` - переменные окружения (опционально)
- `admin/backend/main.py` - CORS настройки

---

**Готово! Проект должен работать.** 🎉

Если что-то не работает, проверьте логи в консоли и раздел "Решение проблем" выше.

