from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, insert

from config import DB_URL
from .models import Base, Tasks, Users

async_engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(async_engine)


async def create_db() -> None:
    async with async_engine.connect() as conn:
        async_engine.echo = False
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        async_engine.echo = True


async def delete_db() -> None:
    async with async_engine.connect() as conn:
        async_engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()
        async_engine.echo = True


async def create_user(tg_id: int, username: str) -> None:
    async with async_session() as session:
        stmt = insert(Users).values(tg_id=tg_id, username=username)
        await session.execute(stmt)
        await session.commit()


async def check_user_exists(tg_id: int) -> bool:
    async with async_session() as session:
        try:
            stmt = select(Users).where(tg_id=tg_id)
            await session.execute(stmt)
        except NoResultFound:
            return False
        return True


async def all_tasks(tg_id: int):
    async with async_session() as session:
        stmt = select(Tasks).where(Tasks.user == tg_id)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        print(tasks)
    return tasks


async def add_task(tg_id, title, body):
    async with async_session() as session:
        stmt = insert(Tasks).values(user=tg_id, title=title, body=body)
        await session.execute(stmt)
        await session.commit()


async def delete_task(tg_id, task_id):
    async with async_session() as session:
        stmt = select(Tasks).where(Tasks.user == tg_id)
