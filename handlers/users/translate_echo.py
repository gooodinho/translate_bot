import googletrans
from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.choose_keyboard import choose_lang, lang
from loader import dp, bot, db

from googletrans import Translator


@dp.message_handler(Command("lang"))
async def change_msg(message: types.Message):
    await message.answer("Выберите новый язык для перевода:", reply_markup=choose_lang)


@dp.message_handler()
async def bot_echo(message: types.Message):
    translator = Translator()
    # print(googletrans.LANGUAGES)
    id = message.from_user.id
    translate = await db.get_translate(id)
    result = translator.translate(message.text, dest=translate.get("translate"))
    await message.answer(result.text)


@dp.callback_query_handler(lang.filter())
async def change_lang(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    id = call.message.chat.id
    short_name = callback_data.get("short_name")
    name = callback_data.get("name")
    await db.update_user_translate(short_name, id)
    await call.message.delete()
    await bot.send_message(chat_id=call.message.chat.id, text=f"Вы выбрали {name} язык!")


