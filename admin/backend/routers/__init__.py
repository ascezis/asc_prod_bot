from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.database.connection import get_db_connection
from app.database.models import Client, Project

admin_router = APIRouter()

# Зависимость для получения асинхронной сессии
async def get_session() -> AsyncSession:
    async for session in get_db_connection():
        yield session

# Получение всех клиентов
@admin_router.get("/clients")
async def list_clients(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Client))
    clients = result.scalars().all()
    return [
        {
            "id": c.id,
            "telegram_id": c.telegram_id,
            "username": c.username,
            "full_name": c.full_name
        }
        for c in clients
    ]

# Получение всех проектов
@admin_router.get("/projects")
async def list_projects(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return [
        {
            "id": p.id,
            "client_id": p.client_id,
            "project_type": p.project_type,
            "duration_raw": p.duration_raw,
            "duration_final": p.duration_final,
            "services": p.services,
            "deadline": p.deadline,
            "budget": p.budget,
            "source_links": p.source_links,
            "style_examples": p.style_examples,
            "additional_notes": p.additional_notes,
            "status": p.status,
            "created_at": str(p.created_at),
            "updated_at": str(p.updated_at) if p.updated_at else None
        }
        for p in projects
    ]
