from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy import select

from config import get_db_url
from .models import Base

async_engine = create_async_engine(url=get_db_url(), echo=True)
async_session = async_sessionmaker(async_engine)


async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# async def get_all_tasks():
#     async with async_session() as session:
#         tasks = select(Tasks).where(tg_id=)
#         await session.commit()