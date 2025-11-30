# Следующие шаги после создания владельца

## ✅ Что уже сделано

1. ✅ Модель User создана в БД
2. ✅ Система аутентификации реализована (JWT токены)
3. ✅ Система авторизации с ролями (User, Admin, Owner)
4. ✅ API endpoints защищены
5. ✅ Владелец создан (ascezis)

---

## 🚀 Шаг 1: Запустить Backend

```bash
python run.py
```

Или отдельно:
```bash
cd admin/backend
uvicorn main:app --reload --port 8000
```

Backend должен запуститься на `http://localhost:8000`

---

## 🧪 Шаг 2: Проверить работу API

### 2.1. Проверить Swagger UI

Откройте в браузере:
```
http://localhost:8000/docs
```

Здесь вы увидите все доступные endpoints и сможете протестировать их.

### 2.2. Войти в систему

**Через Swagger:**
1. Откройте `/auth/login`
2. Нажмите "Try it out"
3. Введите:
   - `username`: `ascezis`
   - `password`: ваш пароль
4. Нажмите "Execute"
5. Скопируйте `access_token` из ответа

**Или через curl:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ascezis&password=ваш_пароль"
```

### 2.3. Проверить защищенные endpoints

**Получить информацию о текущем пользователе:**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"
```

**Получить список клиентов:**
```bash
curl -X GET "http://localhost:8000/clients/" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"
```

**Попробовать без токена (должна быть ошибка 401):**
```bash
curl -X GET "http://localhost:8000/clients/"
```

---

## 📋 Шаг 3: Проверить права доступа

### Тест 1: Owner может удалять проекты
```bash
# Удалить проект (только Owner)
curl -X DELETE "http://localhost:8000/projects/1" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"
```

### Тест 2: Создать нового пользователя (только Owner)
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Authorization: Bearer ВАШ_ТОКЕН" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_test",
    "email": "admin@test.com",
    "password": "test123",
    "role": "admin"
  }'
```

### Тест 3: Получить статистику (только Admin/Owner)
```bash
curl -X GET "http://localhost:8000/statistics/" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"
```

---

## 🎨 Шаг 4: Обновить Frontend (опционально)

Сейчас frontend не поддерживает аутентификацию. Нужно:

1. **Создать страницу входа** (`admin/frontend/src/pages/Login.jsx`)
2. **Добавить сохранение токена** в localStorage
3. **Добавить заголовок Authorization** во все API запросы
4. **Добавить проверку токена** при загрузке приложения
5. **Добавить редирект на логин** если токен отсутствует/невалиден

---

## 📊 Матрица прав доступа

| Endpoint | Без токена | User | Admin | Owner |
|----------|-----------|------|-------|-------|
| `POST /auth/login` | ✅ | ✅ | ✅ | ✅ |
| `GET /auth/me` | ❌ | ✅ | ✅ | ✅ |
| `GET /clients/` | ❌ | ✅ | ✅ | ✅ |
| `POST /clients/` | ❌ | ❌ | ✅ | ✅ |
| `DELETE /clients/{id}` | ❌ | ❌ | ❌ | ✅ |
| `GET /projects/` | ❌ | ✅ | ✅ | ✅ |
| `POST /projects/` | ❌ | ❌ | ✅ | ✅ |
| `DELETE /projects/{id}` | ❌ | ❌ | ❌ | ✅ |
| `GET /statistics/` | ❌ | ❌ | ✅ | ✅ |
| `POST /auth/register` | ❌ | ❌ | ❌ | ✅ |

---

## 🔍 Быстрая проверка через Python

Создайте файл `quick_test.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Вход
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "ascezis", "password": "ваш_пароль"}
)
token = response.json()["access_token"]
print(f"✅ Токен получен: {token[:50]}...")

# 2. Проверка /auth/me
response = requests.get(
    f"{BASE_URL}/auth/me",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"✅ /auth/me: {response.json()}")

# 3. Проверка /clients/
response = requests.get(
    f"{BASE_URL}/clients/",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"✅ /clients/: {len(response.json())} клиентов")

# 4. Проверка без токена (должна быть ошибка)
response = requests.get(f"{BASE_URL}/clients/")
print(f"✅ Без токена: {response.status_code} (должно быть 401)")
```

---

## ⚙️ Настройка JWT_SECRET_KEY

**Важно:** Добавьте в `.env`:

```env
JWT_SECRET_KEY=your-very-secret-key-minimum-32-characters-long
```

Или используйте команду для генерации:
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 📝 Следующие задачи

- [ ] Запустить backend
- [ ] Протестировать вход через Swagger
- [ ] Проверить работу защищенных endpoints
- [ ] Создать тестового Admin пользователя
- [ ] Обновить frontend для работы с аутентификацией
- [ ] Добавить страницу входа в админ-панель

---

**Готово к использованию!** 🎉

