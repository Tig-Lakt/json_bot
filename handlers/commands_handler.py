from aiogram import types
from aiogram.filters.command import Command
from aiogram import Router
from config import *
from sqlalchemy import text
from functions.clean_sql_query import clean_sql_query
from functions.get_sql_from_llm import get_sql_from_llm
from database.database import db_init


router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот готов. Задайте вопрос по аналитике видео на русском языке.")


@router.message()
async def handle_query(message: types.Message):
    try:
        async_session = db_init()        
        raw_sql_query = get_sql_from_llm(message.text)
        sql_query = clean_sql_query(raw_sql_query)
        
        async with async_session[1]() as session:
            result = await session.execute(text(sql_query))
            value = result.scalar()

        if value is None:
            value = 0
        
        await message.answer(f"{value}")
        
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке запроса.")
        print(f"Error: {e}")