"""
Система аутентификации и авторизации
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db_connection
from app.database.models import User, UserRole

# Настройки JWT
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-key-in-production-use-env-file")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 дней

# Настройки для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    # Используем прямой вызов bcrypt для совместимости
    import bcrypt
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    # bcrypt ограничивает пароль до 72 байт
    # Обрезаем пароль, если он длиннее
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Используем прямой вызов bcrypt для обхода проблем с passlib
    import bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создание JWT токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_by_username(username: str, db: AsyncSession) -> Optional[User]:
    """Получить пользователя по username"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def authenticate_user(username: str, password: str, db: AsyncSession) -> Optional[User]:
    """Аутентификация пользователя"""
    user = await get_user_by_username(username, db)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_connection)
) -> User:
    """Получить текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username(username, db)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Получить активного пользователя"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Декораторы для проверки прав доступа
def require_role(*allowed_roles: UserRole):
    """Декоратор для проверки роли пользователя"""
    # Преобразуем Enum в строки для сравнения
    allowed_role_values = [role.value if isinstance(role, UserRole) else role for role in allowed_roles]
    
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        # current_user.role теперь строка, сравниваем со строковыми значениями
        user_role = current_user.role if isinstance(current_user.role, str) else current_user.role.value
        if user_role not in allowed_role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


# Готовые зависимости для разных ролей
def require_admin():
    """Требует роль Admin или Owner"""
    return require_role(UserRole.ADMIN, UserRole.OWNER)


def require_owner():
    """Требует роль Owner"""
    return require_role(UserRole.OWNER)


def require_user():
    """Требует любую роль (User, Admin, Owner)"""
    return require_role(UserRole.USER, UserRole.ADMIN, UserRole.OWNER)

