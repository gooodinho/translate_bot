from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

lang = CallbackData("lang", "short_name", "name")


choose_lang = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Анлгийский",
                    callback_data=lang.new(short_name="en", name="Анлгийский")),

                InlineKeyboardButton(
                    text="Французкий",
                    callback_data=lang.new(short_name="fr", name="Французкий")
                )
            ]
        ]
    )
