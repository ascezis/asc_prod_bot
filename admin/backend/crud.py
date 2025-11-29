from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Client, Project

async def get_clients(session: AsyncSession):
    result = await session.execute(select(Client))
    return result.scalars().all()

async def get_projects(session: AsyncSession):
    result = await session.execute(select(Project))
    return result.scalars().all()
