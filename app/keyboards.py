from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мои задачи')],
        [KeyboardButton(text='Время напоминания о задачах')],
    ],
    resize_keyboard=True
)
