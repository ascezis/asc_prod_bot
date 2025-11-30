# Web App - Локальное тестирование

## Быстрый старт

### 1. Установите ngrok

Скачайте: https://ngrok.com/download

### 2. Запустите Web App сервер

```bash
python app/webapp/server.py
```

Сервер на `http://localhost:8080`

### 3. Запустите ngrok

```bash
ngrok http 8080
```

Скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)

### 4. Обновите URL в боте

В файлах `app/bot/handlers/start.py` и `app/bot/handlers/webapp.py` замените:
```python
web_app_url = "https://abc123.ngrok.io/index.html"
```

### 5. Для backend (если нужен отдельный туннель)

```bash
ngrok http 8000
```

Обновите `API_URL` в `app/webapp/app.js` если используете отдельный туннель.

### 6. Проверьте CORS

В `admin/backend/main.py` уже добавлены ngrok домены в CORS.

## Готово!

Отправьте `/start` боту и нажмите "📱 Создать через Web App"

