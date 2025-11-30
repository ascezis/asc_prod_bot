"""
Роутер для управления пользователями
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.database.connection import get_db_connection
from app.database.models import User, UserRole
from admin.backend.auth import require_admin, require_owner, get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


class UserUpdate(BaseModel):
    """Схема обновления пользователя"""
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Схема ответа пользователя"""
    id: int
    username: str
    email: str
    role: str
    telegram_id: Optional[int] = None
    is_active: bool
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[UserResponse])
async def list_users(
    search: Optional[str] = Query(None, description="Поиск по username или email"),
    role: Optional[str] = Query(None, description="Фильтр по роли"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin())  # Только Admin и Owner
):
    """Список всех пользователей"""
    query = select(User)
    
    # Фильтр по поиску
    if search:
        query = query.where(
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    # Фильтр по роли
    if role:
        query = query.where(User.role == role)
    
    # Применяем пагинацию
    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            telegram_id=user.telegram_id,
            is_active=user.is_active,
            created_at=user.created_at.isoformat() if user.created_at else None
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin())
):
    """Получить информацию о пользователе"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        telegram_id=user.telegram_id,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else None
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin())
):
    """Обновить информацию о пользователе"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем права: только Owner может менять роли и статус
    if user_data.role is not None or user_data.is_active is not None:
        if current_user.role != UserRole.OWNER.value:
            raise HTTPException(
                status_code=403,
                detail="Only Owner can change user roles and status"
            )
    
    # Обновляем поля
    if user_data.email is not None:
        # Проверяем уникальность email
        result = await db.execute(
            select(User).where(User.email == user_data.email, User.id != user_id)
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        user.email = user_data.email
    
    if user_data.role is not None:
        valid_roles = [UserRole.USER.value, UserRole.ADMIN.value, UserRole.OWNER.value]
        if user_data.role not in valid_roles:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role. Must be one of: {valid_roles}"
            )
        user.role = user_data.role
    
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        telegram_id=user.telegram_id,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else None
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_owner())  # Только Owner может удалять
):
    """Удалить пользователя"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Нельзя удалить самого себя
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )
    
    await db.delete(user)
    await db.commit()
    
    return {"detail": "User deleted successfully"}

