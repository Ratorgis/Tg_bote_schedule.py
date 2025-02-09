import asyncio
import os

from aiogram.types import Message
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, F

from kbds import reply
from handlerstg.All_commands import user_router

# инициализация бота + забрал токен 
load_dotenv(find_dotenv())
dp = Dispatcher()
bot = Bot(token=os.getenv("Token"))

# добавление первых команд через роутер, команды heandlerstg/First_commands.py
dp.include_router(user_router)


# команда возвращение к main_кнопкам
@dp.message(F.text.lower() == "вернутся")
async def first_back(message: Message):
    await message.answer("Хорошо", reply_markup=reply.main_kb)


@dp.message(F.text.lower() == "назад")
async def seconde_back(message: Message):
    await message.answer("Хорошо", reply_markup=reply.timetable_kb)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
