import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

from config.config import TOKEN
from aiogram import Bot, Dispatcher, Router
from handlers import commands_handler
import logging
from database.database import create_tables
from functions.load_data_async import read_json

logging.basicConfig(level=logging.INFO)


async def main():
    await create_tables()
    await read_json()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(
                    commands_handler.router
                    )


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)