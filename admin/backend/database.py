from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://video_user:ascezis_pass@localhost/video_editor_bot"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session
