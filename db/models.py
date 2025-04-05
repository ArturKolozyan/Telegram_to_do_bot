from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import BigInteger


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)

    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='user')

    def __repr__(self):
        return f'<Users obj tg_id={self.tg_id}>'


class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(255))
    user_tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'))
    user: Mapped['Users'] = relationship('Users', back_populates='tasks')

    def __repr__(self):
        return f'<Tasks obj title={self.title}>'





