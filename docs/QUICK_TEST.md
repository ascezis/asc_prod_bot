# Быстрый тест системы аутентификации

## Шаг 1: Установить зависимости (если еще не установлены)

```bash
pip install -r admin/backend/requirements.txt
```

## Шаг 2: Запустить Backend

**Вариант A: Только Backend**
```bash
cd admin/backend
uvicorn main:app --reload --port 8000
```

**Вариант B: Все компоненты**
```bash
python run.py
```

## Шаг 3: Проверить работу

### Через браузер:
1. Откройте: `http://localhost:8000/docs`
2. Найдите endpoint `/auth/login`
3. Нажмите "Try it out"
4. Введите:
   - `username`: `ascezis`
   - `password`: ваш пароль
5. Нажмите "Execute"
6. Скопируйте `access_token` из ответа

### Через Python скрипт:
```bash
python test_login.py
```

Введите:
- Username: `ascezis`
- Password: ваш пароль

### Через curl (если установлен):
```bash
curl -X POST "http://localhost:8000/auth/login" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=ascezis&password=ваш_пароль"
```

## Шаг 4: Использовать токен

После получения токена, используйте его для доступа к защищенным endpoints:

```bash
# Получить информацию о пользователе
curl -X GET "http://localhost:8000/auth/me" ^
  -H "Authorization: Bearer ВАШ_ТОКЕН"

# Получить список клиентов
curl -X GET "http://localhost:8000/clients/" ^
  -H "Authorization: Bearer ВАШ_ТОКЕН"
```

## Ожидаемый результат

✅ **Успешный вход:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "ascezis",
    "email": "writerzzz@mail.ru",
    "role": "owner"
  }
}
```

❌ **Ошибка входа (неверный пароль):**
```json
{
  "detail": "Incorrect username or password"
}
```

---

**Готово!** Теперь система аутентификации работает. 🎉

