import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.handlers import router
from db.db import DbOperations


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    logging.basicConfig(level='INFO')
    await DbOperations.delete_db()
    await DbOperations.create_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
