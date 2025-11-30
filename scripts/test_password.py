"""
Тест проверки пароля для пользователя
"""
import asyncio
from app.database.connection import AsyncSessionLocal
from app.database.models import User
from admin.backend.auth import verify_password, get_password_hash
from sqlalchemy.future import select

async def test_password():
    """Тестирование пароля пользователя"""
    username = input("Username для проверки: ").strip()
    password = input("Password для проверки: ").strip()
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        
        if not user:
            print(f"[ERROR] Пользователь '{username}' не найден!")
            return
        
        print(f"\n[INFO] Найден пользователь:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  Hashed password (первые 50 символов): {user.hashed_password[:50]}...")
        
        # Проверяем пароль
        print(f"\n[TEST] Проверка пароля...")
        is_valid = verify_password(password, user.hashed_password)
        
        if is_valid:
            print("[SUCCESS] Пароль верный!")
        else:
            print("[ERROR] Пароль неверный!")
            print(f"\n[DEBUG] Попробуем создать новый хеш для сравнения:")
            new_hash = get_password_hash(password)
            print(f"  Новый хеш: {new_hash[:50]}...")
            print(f"  Старый хеш: {user.hashed_password[:50]}...")
            print(f"  Совпадают: {new_hash == user.hashed_password}")

if __name__ == "__main__":
    asyncio.run(test_password())

