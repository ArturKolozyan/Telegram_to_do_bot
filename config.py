import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
DB_HOSTNAME = os.getenv('DB_HOSTNAME', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'telegram_to_do_bot')
BOT_TOKEN = os.getenv('BOT_TOKEN', '8561202842:AAHhrQ4bmwVzkkQab5wUAOFvvESnQMcBX40')

DB_URL = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'