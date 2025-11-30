"""
Универсальный скрипт для создания пользователей с любой ролью
Использование: python scripts/create_user.py
"""
import asyncio
import sys
import bcrypt
from app.database.connection import AsyncSessionLocal, init_db, engine
from app.database.models import User, UserRole
from sqlalchemy.future import select


def get_password_hash(password: str) -> str:
    """Хеширование пароля с использованием bcrypt напрямую"""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


async def create_user():
    """Создает пользователя с указанной ролью"""
    # Инициализируем БД
    print("[INFO] Инициализация базы данных...")
    await init_db()
    print("[OK] База данных готова\n")
    
    async with AsyncSessionLocal() as session:
        # Показываем доступные роли
        print("=== Доступные роли ===")
        print("1. user   - Заказчик (может просматривать свою информацию)")
        print("2. admin  - Администратор (полный доступ к админке)")
        print("3. owner  - Владелец (полный контроль)\n")
        
        # Запрашиваем данные
        print("=== Создание пользователя ===")
        username = input("Username: ").strip()
        if not username:
            print("[ERROR] Username не может быть пустым!")
            return
        
        email = input("Email: ").strip()
        if not email:
            print("[ERROR] Email не может быть пустым!")
            return
        
        password = input("Password: ").strip()
        if not password:
            print("[ERROR] Password не может быть пустым!")
            return
        
        # Выбор роли
        print("\nВыберите роль:")
        print("1 - user")
        print("2 - admin")
        print("3 - owner")
        role_choice = input("Роль (1/2/3): ").strip()
        
        role_map = {
            "1": UserRole.USER.value,
            "2": UserRole.ADMIN.value,
            "3": UserRole.OWNER.value
        }
        
        if role_choice not in role_map:
            print(f"[ERROR] Неверный выбор роли!")
            return
        
        selected_role = role_map[role_choice]
        
        # Проверяем, не существует ли уже такой пользователь
        result = await session.execute(select(User).where(User.username == username))
        if result.scalars().first():
            print(f"[ERROR] Пользователь с username '{username}' уже существует!")
            return
        
        result = await session.execute(select(User).where(User.email == email))
        if result.scalars().first():
            print(f"[ERROR] Пользователь с email '{email}' уже существует!")
            return
        
        # Создаем пользователя
        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            role=selected_role,
            is_active=True
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        print(f"\n[SUCCESS] Пользователь создан!")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"\nТеперь вы можете войти в админ-панель с этими данными.")


if __name__ == "__main__":
    try:
        asyncio.run(create_user())
    except KeyboardInterrupt:
        print("\n[INFO] Прервано пользователем")
    except Exception as e:
        print(f"\n[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        asyncio.run(engine.dispose())

