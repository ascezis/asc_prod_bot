# admin/backend/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, func
from typing import List, Optional
from app.database.connection import get_db_connection
from app.database.models import Client, Project
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/clients", tags=["clients"])

# -----------------------------
# Pydantic схемы
# -----------------------------
class ClientCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None

class ClientUpdate(BaseModel):
    telegram_id: Optional[int] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

class ClientResponse(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str]
    full_name: Optional[str]
    created_at: datetime
    projects_count: Optional[int] = 0

    class Config:
        from_attributes = True

# -----------------------------
# Роуты
# -----------------------------

@router.get("/", response_model=List[ClientResponse])
async def list_clients(
    search: Optional[str] = Query(None, description="Поиск по username или full_name"),
    telegram_id: Optional[int] = Query(None, description="Фильтр по telegram_id"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    db: AsyncSession = Depends(get_db_connection)
):
    """
    Список клиентов с поиском и фильтрацией
    """
    query = select(Client)
    
    # Поиск по тексту
    if search:
        search_filter = or_(
            Client.username.ilike(f"%{search}%"),
            Client.full_name.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Фильтр по telegram_id
    if telegram_id:
        query = query.where(Client.telegram_id == telegram_id)
    
    # Подсчет проектов для каждого клиента
    projects_count_subquery = select(
        Project.client_id,
        func.count(Project.id).label("count")
    ).group_by(Project.client_id).subquery()
    
    # Применяем лимит и offset
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    clients = result.scalars().all()
    
    # Получаем количество проектов для каждого клиента
    projects_count_query = select(
        Project.client_id,
        func.count(Project.id).label("count")
    ).group_by(Project.client_id)
    projects_result = await db.execute(projects_count_query)
    projects_counts = {row.client_id: row.count for row in projects_result.all()}
    
    # Формируем ответ
    response = []
    for client in clients:
        client_dict = {
            "id": client.id,
            "telegram_id": client.telegram_id,
            "username": client.username,
            "full_name": client.full_name,
            "created_at": client.created_at,
            "projects_count": projects_counts.get(client.id, 0)
        }
        response.append(client_dict)
    
    return response


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    """
    Получить клиента по ID
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalars().first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Подсчет проектов
    projects_count_query = select(func.count(Project.id)).where(Project.client_id == client_id)
    projects_count_result = await db.execute(projects_count_query)
    projects_count = projects_count_result.scalar() or 0
    
    return {
        "id": client.id,
        "telegram_id": client.telegram_id,
        "username": client.username,
        "full_name": client.full_name,
        "created_at": client.created_at,
        "projects_count": projects_count
    }


@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db_connection)
):
    """
    Создание нового клиента
    """
    # Проверяем, не существует ли уже клиент с таким telegram_id
    existing = await db.execute(
        select(Client).where(Client.telegram_id == client_data.telegram_id)
    )
    if existing.scalars().first():
        raise HTTPException(
            status_code=400,
            detail=f"Client with telegram_id {client_data.telegram_id} already exists"
        )
    
    client = Client(**client_data.dict())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    
    return {
        "id": client.id,
        "telegram_id": client.telegram_id,
        "username": client.username,
        "full_name": client.full_name,
        "created_at": client.created_at,
        "projects_count": 0
    }


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: AsyncSession = Depends(get_db_connection)
):
    """
    Обновление клиента
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalars().first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Проверяем уникальность telegram_id, если он изменяется
    if client_data.telegram_id and client_data.telegram_id != client.telegram_id:
        existing = await db.execute(
            select(Client).where(Client.telegram_id == client_data.telegram_id)
        )
        if existing.scalars().first():
            raise HTTPException(
                status_code=400,
                detail=f"Client with telegram_id {client_data.telegram_id} already exists"
            )
    
    # Обновляем поля
    for key, value in client_data.dict(exclude_unset=True).items():
        setattr(client, key, value)
    
    await db.commit()
    await db.refresh(client)
    
    # Подсчет проектов
    projects_count_query = select(func.count(Project.id)).where(Project.client_id == client_id)
    projects_count_result = await db.execute(projects_count_query)
    projects_count = projects_count_result.scalar() or 0
    
    return {
        "id": client.id,
        "telegram_id": client.telegram_id,
        "username": client.username,
        "full_name": client.full_name,
        "created_at": client.created_at,
        "projects_count": projects_count
    }


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db_connection)
):
    """
    Удаление клиента
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalars().first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Проверяем, есть ли у клиента проекты
    projects_count_query = select(func.count(Project.id)).where(Project.client_id == client_id)
    projects_count_result = await db.execute(projects_count_query)
    projects_count = projects_count_result.scalar() or 0
    
    if projects_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete client with {projects_count} projects. Delete projects first."
        )
    
    await db.delete(client)
    await db.commit()
    
    return {"detail": "Client deleted successfully"}

