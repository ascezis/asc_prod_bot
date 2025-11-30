# 🚀 Быстрый запуск проекта

## Вариант 1: Запуск через Electron GUI (рекомендуется)

### Шаг 1: Установка зависимостей

```bash
# Python зависимости
pip install -r requirements.txt
pip install -r admin/backend/requirements.txt

# Frontend зависимости
cd admin/frontend
npm install
cd ../..

# Electron зависимости
cd admin-GUI
npm install
cd ..
```

### Шаг 2: Настройка конфигурации

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_bot_token_here
BOT_ADMIN_ID=your_telegram_user_id
DB_USER=video_user
DB_PASSWORD=ascezis_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=video_editor_bot
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Или отредактируйте `app/config.py` напрямую.

### Шаг 3: Запуск через Electron

```bash
cd admin-GUI
npm start
```

В открывшемся окне нажмите кнопку **"Запуск"** - это запустит:
- ✅ Backend API на `http://localhost:8000`
- ✅ Frontend на `http://localhost:5173`
- ✅ Telegram Bot

Для остановки нажмите **"Остановка"**.

---

## Вариант 2: Запуск через run.py (все компоненты сразу)

### Шаг 1: Установка зависимостей (см. выше)

### Шаг 2: Настройка конфигурации (см. выше)

### Шаг 3: Запуск

```bash
python run.py
```

Это запустит все три компонента одновременно. Для остановки нажмите `Ctrl+C`.

---

## Вариант 3: Запуск компонентов отдельно (для отладки)

### Терминал 1: Backend API

```bash
cd admin/backend
uvicorn main:app --reload --port 8000
```

Backend будет доступен на: `http://localhost:8000`
- API документация: `http://localhost:8000/docs`

### Терминал 2: Frontend

```bash
cd admin/frontend
npm run dev
```

Frontend будет доступен на: `http://localhost:5173` (или другой порт Vite)

### Терминал 3: Telegram Bot

```bash
python -m app.main
```

---

## Проверка работы

### Backend
- Откройте: `http://localhost:8000/docs` - Swagger UI
- Проверьте: `http://localhost:8000/statistics/` - статистика

### Frontend
- Откройте: `http://localhost:5173`
- Проверьте работу Dashboard, Clients, Projects

### Bot
- Откройте Telegram
- Найдите вашего бота
- Отправьте `/start`

---

## Требования перед запуском

1. ✅ PostgreSQL запущен и доступен
2. ✅ База данных создана (см. README.md)
3. ✅ Все зависимости установлены
4. ✅ Конфигурация настроена (`.env` или `app/config.py`)
5. ✅ Telegram Bot Token получен
6. ✅ Node.js и npm установлены

---

## Решение проблем

### Ошибка "Module not found"
```bash
pip install -r requirements.txt
pip install -r admin/backend/requirements.txt
```

### Ошибка подключения к БД
- Проверьте, что PostgreSQL запущен
- Проверьте настройки в `config.py` или `.env`
- Убедитесь, что база данных создана

### Frontend не запускается
```bash
cd admin/frontend
npm install
npm run dev
```

### Backend не запускается
```bash
cd admin/backend
pip install fastapi uvicorn[standard]
uvicorn main:app --reload --port 8000
```

### Бот не отвечает
- Проверьте `BOT_TOKEN` в конфигурации
- Убедитесь, что бот запущен (проверьте логи)
- Проверьте интернет-соединение

---

## Порты по умолчанию

- **Backend API**: `8000`
- **Frontend**: `5173` (Vite)
- **PostgreSQL**: `5432`

Если порты заняты, измените их в соответствующих конфигурационных файлах.

