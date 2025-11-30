# Руководство по системе аутентификации и авторизации

## 📋 Уровни доступа

### 1. **User** (Заказчик)
- Может просматривать свою информацию
- Может просматривать свои проекты
- **Не может:** создавать, редактировать, удалять данные

### 2. **Admin** (Администратор)
- Полный доступ к админ-панели
- Может просматривать всех клиентов и проекты
- Может создавать и редактировать клиентов и проекты
- Может просматривать статистику
- **Не может:** удалять клиентов/проекты, создавать пользователей

### 3. **Owner** (Владелец)
- Все права Admin
- Может удалять клиентов и проекты
- Может создавать новых пользователей (Admin, User, Owner)
- Может управлять модулями системы
- Полный контроль над системой

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 2. Настройка SECRET_KEY

Добавьте в `.env` файл:
```env
JWT_SECRET_KEY=your-very-secret-key-here-minimum-32-characters
```

**Важно:** Используйте надежный случайный ключ в production!

### 3. Создание первого пользователя-владельца

```bash
python create_owner.py
```

Введите:
- Username
- Email
- Password

Будет создан пользователь с ролью **Owner**.

### 4. Вход в систему

Используйте endpoint `/auth/login`:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

Ответ:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "owner",
    "email": "owner@example.com",
    "role": "owner"
  }
}
```

### 5. Использование токена

Добавьте заголовок в запросы:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📡 API Endpoints

### Аутентификация (`/auth`)

- `POST /auth/login` - Вход в систему (публичный)
- `POST /auth/register` - Регистрация (только Owner)
- `GET /auth/me` - Информация о текущем пользователе (требуется авторизация)

### Клиенты (`/clients`)

- `GET /clients/` - Список клиентов (требуется авторизация)
- `GET /clients/{id}` - Получить клиента (требуется авторизация)
- `POST /clients/` - Создать клиента (только Admin/Owner)
- `PUT /clients/{id}` - Обновить клиента (только Admin/Owner)
- `DELETE /clients/{id}` - Удалить клиента (только Owner)

### Проекты (`/projects`)

- `GET /projects/` - Список проектов (требуется авторизация)
- `GET /projects/{id}` - Получить проект (требуется авторизация)
- `POST /projects/` - Создать проект (только Admin/Owner)
- `PUT /projects/{id}` - Обновить проект (только Admin/Owner)
- `DELETE /projects/{id}` - Удалить проект (только Owner)

### Статистика (`/statistics`)

- `GET /statistics/` - Получить статистику (только Admin/Owner)

---

## 🔐 Права доступа по endpoints

| Endpoint | User | Admin | Owner |
|----------|------|-------|-------|
| `GET /clients/` | ✅ | ✅ | ✅ |
| `GET /projects/` | ✅ | ✅ | ✅ |
| `POST /clients/` | ❌ | ✅ | ✅ |
| `PUT /clients/{id}` | ❌ | ✅ | ✅ |
| `DELETE /clients/{id}` | ❌ | ❌ | ✅ |
| `POST /projects/` | ❌ | ✅ | ✅ |
| `PUT /projects/{id}` | ❌ | ✅ | ✅ |
| `DELETE /projects/{id}` | ❌ | ❌ | ✅ |
| `GET /statistics/` | ❌ | ✅ | ✅ |
| `POST /auth/register` | ❌ | ❌ | ✅ |

---

## 💻 Использование в коде

### Проверка прав в роутерах

```python
from admin.backend.auth import require_admin, require_owner, get_current_active_user

# Требуется любая авторизация
@router.get("/")
async def endpoint(current_user: User = Depends(get_current_active_user)):
    ...

# Требуется Admin или Owner
@router.post("/")
async def endpoint(current_user: User = Depends(require_admin())):
    ...

# Требуется только Owner
@router.delete("/{id}")
async def endpoint(current_user: User = Depends(require_owner())):
    ...
```

---

## 🗄️ Модель User

```python
class User(Base):
    id: int
    username: str (unique)
    email: str (unique)
    hashed_password: str
    role: UserRole (user/admin/owner)
    telegram_id: int (optional) - связь с Telegram
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

---

## 🔄 Связь с Telegram

Пользователь может быть связан с Telegram через поле `telegram_id`:
- При создании заявки через бота создается `Client` с `telegram_id`
- Если пользователь зарегистрирован в админке, можно связать `Client.user_id` с `User.id`
- Это позволяет заказчику (User) видеть свои проекты в админ-панели

---

## ⚠️ Важные замечания

1. **SECRET_KEY** должен быть надежным и храниться в `.env`
2. Токены действительны **30 дней**
3. Пароли хешируются с помощью **bcrypt**
4. Все API endpoints (кроме `/auth/login`) требуют авторизации
5. Регистрация новых пользователей доступна только **Owner**

---

## 🧪 Тестирование

### Создание тестового пользователя через Python:

```python
from app.database.connection import AsyncSessionLocal
from app.database.models import User, UserRole
from admin.backend.auth import get_password_hash

async def create_test_user():
    async with AsyncSessionLocal() as session:
        user = User(
            username="test_admin",
            email="admin@test.com",
            hashed_password=get_password_hash("test123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        session.add(user)
        await session.commit()
```

---

## 📝 Следующие шаги

1. ✅ Установить зависимости
2. ✅ Добавить JWT_SECRET_KEY в .env
3. ✅ Создать первого Owner через `create_owner.py`
4. ✅ Обновить frontend для работы с аутентификацией
5. ✅ Добавить страницу входа в админ-панель

