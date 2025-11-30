# admin/backend/routers/statistics.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database.connection import get_db_connection
from app.database.models import Client, Project, AIAnalysis
from pydantic import BaseModel
from typing import Dict, List, Optional

router = APIRouter(prefix="/statistics", tags=["statistics"])

class TopClient(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    projects_count: int

class StatisticsResponse(BaseModel):
    total_clients: int
    total_projects: int
    projects_by_status: Dict[str, int]
    projects_by_type: Dict[str, int]
    recent_projects_count: int  # за последние 7 дней
    total_ai_analyses: int
    average_realism_score: float
    top_clients: List[TopClient]

@router.get("/", response_model=StatisticsResponse)
async def get_statistics(db: AsyncSession = Depends(get_db_connection)):
    """
    Получить общую статистику
    """
    # Общее количество клиентов
    clients_count_result = await db.execute(select(func.count(Client.id)))
    total_clients = clients_count_result.scalar() or 0
    
    # Общее количество проектов
    projects_count_result = await db.execute(select(func.count(Project.id)))
    total_projects = projects_count_result.scalar() or 0
    
    # Проекты по статусам
    status_count_result = await db.execute(
        select(Project.status, func.count(Project.id))
        .group_by(Project.status)
    )
    projects_by_status = {row[0] or "unknown": row[1] for row in status_count_result.all()}
    
    # Проекты по типам
    type_count_result = await db.execute(
        select(Project.project_type, func.count(Project.id))
        .group_by(Project.project_type)
    )
    projects_by_type = {row[0] or "unknown": row[1] for row in type_count_result.all()}
    
    # Проекты за последние 7 дней
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_projects_result = await db.execute(
        select(func.count(Project.id))
        .where(Project.created_at >= seven_days_ago)
    )
    recent_projects_count = recent_projects_result.scalar() or 0
    
    # AI анализы
    ai_count_result = await db.execute(select(func.count(AIAnalysis.id)))
    total_ai_analyses = ai_count_result.scalar() or 0
    
    # Средний realism_score
    avg_score_result = await db.execute(
        select(func.avg(AIAnalysis.realism_score))
        .where(AIAnalysis.realism_score.isnot(None))
    )
    average_realism_score = float(avg_score_result.scalar() or 0)
    
    # Топ клиентов по количеству проектов
    top_clients_result = await db.execute(
        select(
            Client.id,
            Client.telegram_id,
            Client.username,
            Client.full_name,
            func.count(Project.id).label("projects_count")
        )
        .outerjoin(Project, Client.id == Project.client_id)
        .group_by(Client.id, Client.telegram_id, Client.username, Client.full_name)
        .order_by(func.count(Project.id).desc())
        .limit(10)
    )
    top_clients = [
        TopClient(
            id=row.id,
            telegram_id=row.telegram_id,
            username=row.username,
            full_name=row.full_name,
            projects_count=row.projects_count or 0
        )
        for row in top_clients_result.all()
    ]
    
    return {
        "total_clients": total_clients,
        "total_projects": total_projects,
        "projects_by_status": projects_by_status,
        "projects_by_type": projects_by_type,
        "recent_projects_count": recent_projects_count,
        "total_ai_analyses": total_ai_analyses,
        "average_realism_score": round(average_realism_score, 2),
        "top_clients": top_clients
    }

