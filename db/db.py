from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from config import DB_URL
from .models import Base, Tasks, Users

async_engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(async_engine)


class DbOperations:

    @staticmethod
    async def create_db() -> None:
        async with async_engine.connect() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            async_engine.echo = True

    @staticmethod
    async def delete_db() -> None:
        async with async_engine.connect() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.commit()
            async_engine.echo = True


class DbFunctions:

    @staticmethod
    async def create_user(tg_id) -> None:
        async with async_session() as session:
            stmt = insert(Users).values(tg_id=tg_id)
            try:
                await session.execute(stmt)
                await session.commit()
            except IntegrityError:
                return None

    @staticmethod
    async def all_tasks(tg_id):
        async with async_session() as session:
            stmt = select(Users).options(selectinload(Users.tasks)).where(Users.tg_id == tg_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            tasks = user.tasks
            print(tasks)
            return tasks

    @staticmethod
    async def add_task(tg_id, title, body):
        async with async_session() as session:
            stmt = insert(Tasks).values(user_tg_id=tg_id, title=title, body=body)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_task(tg_id, task_i):
        async with async_session() as session:
            stmt = select(Users).options(selectinload(Users.tasks)).where(Users.tg_id == tg_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            task = user.tasks[task_i]
            await session.delete(task)
            await session.commit()
