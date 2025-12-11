from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Задачи')],
    ],
    resize_keyboard=True
)

tasks = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Задачи')],
        [KeyboardButton(text='Добавить задачу'), KeyboardButton(text='Удалить задачу')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)