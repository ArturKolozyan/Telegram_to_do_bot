import datetime

from sqlalchemy import String, BigInteger, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))

class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(255))
    user: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'))
    created: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated: Mapped[datetime.datetime] = mapped_column(default=func.now(), onupdate=func.now())

