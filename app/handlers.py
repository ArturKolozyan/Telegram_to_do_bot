from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
import app.keyboards as kb

import db.db as db


class Task(StatesGroup):
    title = State()
    body = State()


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    tg_id = message.from_user.id
    if db.check_user_exists(tg_id=tg_id):
        await db.create_user(tg_id=tg_id, username=message.from_user.username)
    text = (f'Привет {message.from_user.full_name}!\n'
            f'Это бот для планирования задач')
    await message.answer(text, reply_markup=kb.main)


@router.message(F.text == 'Назад')
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы вернулись назад', reply_markup=kb.main)


@router.message(F.text == 'Задачи')
async def all_tasks_handler(message: Message):
    tasks = await db.all_tasks(message.from_user.id)
    if tasks:
        text = "Ваши задачи:\n"
        for task in tasks:
            text += f"Title: {task.title}\nBody: {task.body}\n\n"
        await message.answer(text, reply_markup=kb.tasks)
    else:
        await message.answer("У вас пока нет задач.", reply_markup=kb.tasks)


@router.message(F.text == 'Добавить задачу')
async def add_task_handler_1(message: Message, state: FSMContext):
    await message.answer('Напишите заголовок задачи', reply_markup=kb.task_add)
    await state.set_state(Task.title)


@router.message(F.text, Task.title)
async def add_task_handler_2(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Напиши содержание задачи')
    await state.set_state(Task.body)


@router.message(F.text, Task.body)
async def add_task_handler_3(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    data = await state.get_data()
    await db.add_task(tg_id=message.from_user.id, title=data.get('title'), body=data.get('body'))
    await message.answer('Вы создали новую задачу', reply_markup=kb.tasks)
    await state.clear()

