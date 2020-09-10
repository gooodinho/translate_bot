from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    id = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username
    user_language = message.from_user.language_code
    await db.add_user(id, name, username, user_language)
    text = """
Привет, я - <b>ECHO-TRANSLATE BOT</b>🤖🔄
    
🔹 Отправь мне сообщение и я переведу его (на Анлгийский).
🔹 Нажми на команду ниже что бы поменять язык.

📍 /lang - Поменять язык перевода
    """
    await message.answer(text)
