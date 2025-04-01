import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.handlers import router
from db.db import create_db, delete_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    await delete_db()
    await create_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
