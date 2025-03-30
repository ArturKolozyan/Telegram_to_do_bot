import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = 'tasks'

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
