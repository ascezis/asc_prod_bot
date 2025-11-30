"""
Упрощенный скрипт для создания первого пользователя-владельца (Owner)
Не требует FastAPI, использует только SQLAlchemy
"""
import asyncio
import sys
import bcrypt
from app.database.connection import AsyncSessionLocal, init_db, engine
from app.database.models import User, UserRole


def get_password_hash(password: str) -> str:
    """Хеширование пароля с использованием bcrypt напрямую"""
    # bcrypt ограничивает пароль до 72 байт
    # Обрезаем пароль, если он длиннее
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Генерируем соль и хешируем пароль
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


async def create_owner():
    """Создает первого пользователя-владельца"""
    # Инициализируем БД (создаст таблицу users, если её нет)
    print("[INFO] Инициализация базы данных...")
    await init_db()
    print("[OK] База данных готова")
    
    async with AsyncSessionLocal() as session:
        from sqlalchemy.future import select
        
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
            role=UserRole.OWNER.value,  # Используем .value для String поля
            is_active=True
        )
        
        session.add(owner)
        await session.commit()
        await session.refresh(owner)
        
        print(f"\n[SUCCESS] Пользователь-владелец создан!")
        print(f"  ID: {owner.id}")
        print(f"  Username: {owner.username}")
        print(f"  Email: {owner.email}")
        print(f"  Role: {owner.role}")
        print(f"\nТеперь вы можете войти в админ-панель с этими данными.")


if __name__ == "__main__":
    try:
        asyncio.run(create_owner())
    except KeyboardInterrupt:
        print("\n[INFO] Прервано пользователем")
    except Exception as e:
        print(f"\n[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Закрываем соединение
        asyncio.run(engine.dispose())

