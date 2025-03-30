from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# from db.db import async_session
# from db.models import Tasks
import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    text = (f'Привет {message.from_user.full_name}!\n'
            f'Это бот для планирования задач')
    await message.answer(text, reply_markup=kb.main)


@router.message(Command('Мои задачи'))
async def my_tasks(message: Message):
    pass