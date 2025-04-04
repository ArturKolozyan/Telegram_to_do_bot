from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import app.keyboards as kb
from db.db import DbFunctions


class TaskCreate(StatesGroup):
    title = State()
    body = State()


class TaskDelete(StatesGroup):
    num = State()


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await DbFunctions.create_user(tg_id=message.from_user.id)
    text = f'Привет {message.from_user.full_name}!\nЭто бот для планирования задач'
    await message.answer(text, reply_markup=kb.main)


@router.message(F.text == 'Назад')
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы вернулись назад', reply_markup=kb.main)


@router.message(F.text == 'Задачи')
async def all_tasks_handler(message: Message):
    tasks = await DbFunctions.all_tasks(message.from_user.id)
    if tasks:
        text = "Ваши задачи:\n"
        for task_i, task in enumerate(tasks, start=1):
            text += f"{task_i}. {task.title}: {task.body}\n"
        await message.answer(text, reply_markup=kb.tasks)
    else:
        await message.answer("У вас пока нет задач", reply_markup=kb.tasks)


@router.message(F.text == 'Добавить задачу')
async def add_task_handler_1(message: Message, state: FSMContext):
    await message.answer('Напишите заголовок задачи', reply_markup=kb.task_add)
    await state.set_state(TaskCreate.title)


@router.message(F.text, TaskCreate.title)
async def add_task_handler_2(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Напиши содержание задачи')
    await state.set_state(TaskCreate.body)


@router.message(F.text, TaskCreate.body)
async def add_task_handler_3(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    data = await state.get_data()
    await DbFunctions.add_task(tg_id=message.from_user.id, title=data.get('title'), body=data.get('body'))
    await message.answer('Вы создали новую задачу', reply_markup=kb.tasks)
    await state.clear()


@router.message(F.text == 'Удалить задачу')
async def delete_task_handler_1(message: Message, state: FSMContext):
    tasks = await DbFunctions.all_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У вас пока нет задач", reply_markup=kb.tasks)
        return

    await state.update_data(tasks=tasks)
    await message.answer('Введите номер задачи')
    await state.set_state(TaskDelete.num)



@router.message(F.text, TaskDelete.num)
async def delete_task_handler_2(message: Message, state: FSMContext):
    task_i = message.text

    if not task_i.isdigit():
        await message.answer('Некорректный номер задачи. Пожалуйста, введите число')
        return

    task_i = int(task_i)

    data = await state.get_data()
    tasks = data.get('tasks')
    if task_i < 1 or task_i > len(tasks):
        await message.answer('Некорректный номер задачи. Пожалуйста, введите существующий номер задачи')
        return

    await DbFunctions.delete_task(message.from_user.id, task_i=task_i)
    await message.answer(f'Удалена задача номер {task_i}')
    await state.clear()

