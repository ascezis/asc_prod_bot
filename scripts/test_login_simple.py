"""
Простой тест входа без FastAPI
"""
import asyncio
import bcrypt
from app.database.connection import AsyncSessionLocal
from app.database.models import User
from sqlalchemy.future import select

async def test_login():
    """Тестирование входа"""
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        
        if not user:
            print(f"[ERROR] Пользователь '{username}' не найден!")
            return
        
        print(f"\n[INFO] Найден пользователь: {user.username} (ID: {user.id})")
        print(f"  Role: {user.role}")
        print(f"  Is active: {user.is_active}")
        
        # Проверяем пароль
        print(f"\n[TEST] Проверка пароля...")
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        hashed_bytes = user.hashed_password.encode('utf-8')
        is_valid = bcrypt.checkpw(password_bytes, hashed_bytes)
        
        if is_valid:
            print("[SUCCESS] Пароль верный! Вход должен работать.")
        else:
            print("[ERROR] Пароль неверный!")
            print(f"\n[DEBUG] Информация:")
            print(f"  Введенный пароль (bytes): {len(password_bytes)} байт")
            print(f"  Хеш в БД (первые 30 символов): {user.hashed_password[:30]}...")
            
            # Попробуем создать новый хеш для сравнения
            salt = bcrypt.gensalt()
            new_hash = bcrypt.hashpw(password_bytes, salt)
            print(f"  Новый хеш (первые 30 символов): {new_hash.decode()[:30]}...")

if __name__ == "__main__":
    try:
        asyncio.run(test_login())
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

