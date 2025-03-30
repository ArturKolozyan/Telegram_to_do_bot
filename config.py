import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

BOT_TOKEN = os.getenv('BOT_TOKEN')


def get_db_url():
    return f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'


def get_bot_token():
    return BOT_TOKEN
