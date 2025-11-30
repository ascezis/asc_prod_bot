"""
Скрипт для создания первого пользователя-владельца (Owner)
Использование: python create_owner.py
"""
import asyncio
import sys
from app.database.connection import AsyncSessionLocal, init_db
from app.database.models import User, UserRole
from admin.backend.auth import get_password_hash
from sqlalchemy.future import select


async def create_owner():
    """Создает первого пользователя-владельца"""
    # Инициализируем БД (создаст таблицу users, если её нет)
    print("[INFO] Инициализация базы данных...")
    await init_db()
    print("[OK] База данных готова")
    
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже пользователи
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        if users:
            print("[WARNING] В системе уже есть пользователи!")
            response = input("Создать нового Owner? (y/n): ")
            if response.lower() != 'y':
                print("Отменено")
                return
        
        # Запрашиваем данные
        print("\n=== Создание пользователя-владельца ===")
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
        owner = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            role=UserRole.OWNER,
            is_active=True
        )
        
        session.add(owner)
        await session.commit()
        await session.refresh(owner)
        
        print(f"\n[SUCCESS] Пользователь-владелец создан!")
        print(f"  ID: {owner.id}")
        print(f"  Username: {owner.username}")
        print(f"  Email: {owner.email}")
        print(f"  Role: {owner.role.value}")
        print(f"\nТеперь вы можете войти в админ-панель с этими данными.")


if __name__ == "__main__":
    asyncio.run(create_owner())

