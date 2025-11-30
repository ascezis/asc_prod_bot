# admin/backend/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from app.database.connection import get_db_connection
from app.database.models import Project, Client, AIAnalysis, User
from admin.backend.auth import require_admin, require_owner, get_current_active_user
from admin.backend.crud import get_projects, get_clients
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["projects"])

# -----------------------------
# Pydantic схемы
# -----------------------------
class ProjectCreate(BaseModel):
    client_id: int
    project_type: str
    duration_raw: str
    duration_final: str
    services: List[str]
    deadline: str
    budget: str
    source_links: Optional[str] = None
    style_examples: Optional[str] = None
    additional_notes: Optional[str] = None
    status: Optional[str] = "new"

class ProjectUpdate(BaseModel):
    project_type: Optional[str] = None
    duration_raw: Optional[str] = None
    duration_final: Optional[str] = None
    services: Optional[List[str]] = None
    deadline: Optional[str] = None
    budget: Optional[str] = None
    source_links: Optional[str] = None
    style_examples: Optional[str] = None
    additional_notes: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    client_id: int
    project_type: str
    duration_raw: str
    duration_final: str
    services: List[str]
    deadline: str
    budget: str
    source_links: Optional[str] = None
    style_examples: Optional[str] = None
    additional_notes: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    client_name: Optional[str] = None

    class Config:
        from_attributes = True

# -----------------------------
# Роуты
# -----------------------------

@router.get("/webapp", response_model=List[ProjectResponse])
async def list_projects_webapp(
    telegram_id: int = Query(..., description="Telegram ID пользователя"),
    db: AsyncSession = Depends(get_db_connection)
):
    """
    Список проектов для Web App (по telegram_id, без авторизации)
    """
    # Находим клиента по telegram_id
    result = await db.execute(select(Client).where(Client.telegram_id == telegram_id))
    client = result.scalars().first()
    
    if not client:
        return []
    
    # Получаем проекты клиента
    result = await db.execute(
        select(Project)
        .where(Project.client_id == client.id)
        .order_by(Project.created_at.desc())
    )
    projects = result.scalars().all()
    
    return [
        ProjectResponse(
            id=p.id,
            client_id=p.client_id,
            project_type=p.project_type,
            duration_raw=p.duration_raw,
            duration_final=p.duration_final,
            services=p.services or [],
            deadline=p.deadline,
            budget=p.budget,
            source_links=p.source_links,
            style_examples=p.style_examples,
            additional_notes=p.additional_notes,
            status=p.status,
            created_at=p.created_at.isoformat() if p.created_at else None,
            updated_at=p.updated_at.isoformat() if p.updated_at else None,
            client_name=client.full_name or client.username or f"User {client.telegram_id}"
        )
        for p in projects
    ]


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    client_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(get_current_active_user)  # Требуется авторизация
):
    """
    Список проектов. Можно фильтровать по client_id и статусу.
    """
    query = select(Project, Client).outerjoin(Client, Project.client_id == Client.id)
    
    # Фильтрация
    if client_id is not None:
        query = query.where(Project.client_id == client_id)
    if status is not None:
        query = query.where(Project.status == status)
    if search:
        query = query.where(
            or_(
                Project.project_type.ilike(f"%{search}%"),
                Project.budget.ilike(f"%{search}%"),
                Project.deadline.ilike(f"%{search}%"),
                Project.additional_notes.ilike(f"%{search}%")
            )
        )
    
    # Пагинация
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    rows = result.all()
    
    # Формируем ответ с именем клиента
    projects = []
    for project, client in rows:
        project_dict = {
            "id": project.id,
            "client_id": project.client_id,
            "project_type": project.project_type,
            "duration_raw": project.duration_raw,
            "duration_final": project.duration_final,
            "services": project.services or [],
            "deadline": project.deadline,
            "budget": project.budget,
            "source_links": project.source_links,
            "style_examples": project.style_examples,
            "additional_notes": project.additional_notes,
            "status": project.status,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "client_name": client.full_name if client else None
        }
        projects.append(project_dict)
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db_connection)):
    """
    Получить одну заявку по ID
    """
    result = await db.execute(
        select(Project, Client)
        .outerjoin(Client, Project.client_id == Client.id)
        .where(Project.id == project_id)
    )
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project, client = row
    return {
        "id": project.id,
        "client_id": project.client_id,
        "project_type": project.project_type,
        "duration_raw": project.duration_raw,
        "duration_final": project.duration_final,
        "services": project.services or [],
        "deadline": project.deadline,
        "budget": project.budget,
        "source_links": project.source_links,
        "style_examples": project.style_examples,
        "additional_notes": project.additional_notes,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "client_name": client.full_name if client else None
    }


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate, 
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin())  # Только Admin и Owner
):
    """
    Создание новой заявки
    """
    project = Project(**project_data.dict())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    # Получаем клиента для имени
    client_result = await db.execute(select(Client).where(Client.id == project.client_id))
    client = client_result.scalars().first()
    
    return {
        "id": project.id,
        "client_id": project.client_id,
        "project_type": project.project_type,
        "duration_raw": project.duration_raw,
        "duration_final": project.duration_final,
        "services": project.services or [],
        "deadline": project.deadline,
        "budget": project.budget,
        "source_links": project.source_links,
        "style_examples": project.style_examples,
        "additional_notes": project.additional_notes,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "client_name": client.full_name if client else None
    }


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int, 
    project_data: ProjectUpdate, 
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_admin())  # Только Admin и Owner
):
    """
    Обновление заявки
    """
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project, key, value)
    
    await db.commit()
    await db.refresh(project)
    
    # Получаем клиента для имени
    client_result = await db.execute(select(Client).where(Client.id == project.client_id))
    client = client_result.scalars().first()
    
    return {
        "id": project.id,
        "client_id": project.client_id,
        "project_type": project.project_type,
        "duration_raw": project.duration_raw,
        "duration_final": project.duration_final,
        "services": project.services or [],
        "deadline": project.deadline,
        "budget": project.budget,
        "source_links": project.source_links,
        "style_examples": project.style_examples,
        "additional_notes": project.additional_notes,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "client_name": client.full_name if client else None
    }


@router.delete("/{project_id}")
async def delete_project(
    project_id: int, 
    db: AsyncSession = Depends(get_db_connection),
    current_user: User = Depends(require_owner())  # Только Owner
):
    """
    Удаление заявки (с удалением связанных AI анализов)
    """
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Сначала удаляем все связанные AI анализы
    ai_analyses_result = await db.execute(
        select(AIAnalysis).where(AIAnalysis.project_id == project_id)
    )
    ai_analyses = ai_analyses_result.scalars().all()
    
    for analysis in ai_analyses:
        await db.delete(analysis)
    
    # Затем удаляем сам проект
    await db.delete(project)
    await db.commit()
    
    return {"detail": "Project deleted successfully"}
