"""
Роутер для аутентификации
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.database.connection import get_db_connection
from app.database.models import User, UserRole
from admin.backend.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_active_user,
    require_owner,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserCreate(BaseModel):
    """Схема создания пользователя"""
    username: str
    email: EmailStr
    password: str
    role: str = UserRole.USER.value  # Используем строковое значение


class UserResponse(BaseModel):
    """Схема ответа пользователя"""
    id: int
    username: str
    email: str
    role: str  # Изменено на str, так как в БД хранится строка
    telegram_id: Optional[int] = None
    is_active: bool
    
    class Config:
        from_attributes = True


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_connection)
):
    """Вход в систему"""
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # user.role теперь строка, не Enum
    role_value = user.role if isinstance(user.role, str) else user.role.value
    access_token = create_access_token(
        data={"sub": user.username, "role": role_value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role_value
        }
    }


class UserRegister(BaseModel):
    """Схема публичной регистрации (только для роли User)"""
    username: str
    email: EmailStr
    password: str


@router.post("/register", response_model=UserResponse)
async def register_public(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db_connection)
):
    """Публичная регистрация нового пользователя (только роль User)"""
    from sqlalchemy.future import select
    
    # Проверяем, существует ли пользователь
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаем пользователя только с ролью User
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=UserRole.USER.value,  # Всегда User для публичной регистрации
        is_active=True
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Возвращаем пользователя с правильным форматом
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,  # Уже строка
        telegram_id=user.telegram_id,
        is_active=user.is_active
    )


@router.post("/register/admin", response_model=UserResponse)
async def register_admin(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_owner())  # Только Owner может создавать пользователей с любой ролью
):
    """Регистрация нового пользователя с любой ролью (только для Owner)"""
    from sqlalchemy.future import select
    
    # Проверяем, существует ли пользователь
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Проверяем, что роль валидна
    valid_roles = [UserRole.USER.value, UserRole.ADMIN.value, UserRole.OWNER.value]
    if user_data.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {valid_roles}"
        )
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=True
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Возвращаем пользователя с правильным форматом
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,  # Уже строка
        telegram_id=user.telegram_id,
        is_active=user.is_active
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Получить информацию о текущем пользователе"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,  # Уже строка
        telegram_id=current_user.telegram_id,
        is_active=current_user.is_active
    )

