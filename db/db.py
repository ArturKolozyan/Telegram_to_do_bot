from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, insert

from config import DB_URL
from .models import Base, Tasks

async_engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(async_engine)


async def create_db():
    async with async_engine.connect() as conn:
        async_engine.echo = False
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        async_engine.echo = True


async def delete_db():
    async with async_engine.connect() as conn:
        async_engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()
        async_engine.echo = True


async def all_tasks(tg_id):
    async with async_session() as session:
        stmt = select(Tasks).where(Tasks.tg_id == tg_id)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
    return tasks


async def add_task(tg_id, title, body):
    async with async_session() as session:
        stmt = insert(Tasks).values(tg_id=tg_id, title=title, body=body)
        await session.execute(stmt)
        await session.commit()


# async def delete_task(tg_id):
#     async with async_session() as session:
#         stmt = select()