from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from app.database.models import Client, Project

# -------------------
# Получение всех клиентов
# -------------------
async def get_clients(session: AsyncSession):
    result = await session.execute(select(Client))
    return result.scalars().all()

# -------------------
# Получение всех проектов
# -------------------
async def get_projects(session: AsyncSession):
    result = await session.execute(select(Project))
    return result.scalars().all()

# -------------------
# Получение проекта по ID
# -------------------
async def get_project(session: AsyncSession, project_id: int) -> Project | None:
    result = await session.execute(select(Project).where(Project.id == project_id))
    return result.scalars().first()

# -------------------
# Создание новой заявки
# -------------------
async def create_project(session: AsyncSession, project_data: dict) -> Project:
    project = Project(**project_data)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project

# -------------------
# Обновление заявки
# -------------------
async def update_project(session: AsyncSession, project_id: int, update_data: dict) -> Project | None:
    await session.execute(
        update(Project)
        .where(Project.id == project_id)
        .values(**update_data)
    )
    await session.commit()
    return await get_project(session, project_id)

# -------------------
# Удаление заявки
# -------------------
async def delete_project(session: AsyncSession, project_id: int) -> bool:
    await session.execute(delete(Project).where(Project.id == project_id))
    await session.commit()
    return True

# -------------------
# Фильтрация заявок
# -------------------
async def filter_projects(session: AsyncSession, **filters) -> list[Project]:
    query = select(Project)
    for attr, value in filters.items():
        if hasattr(Project, attr):
            query = query.where(getattr(Project, attr) == value)
    result = await session.execute(query)
    return result.scalars().all()
