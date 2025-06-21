from aiogram import types
from aiogram.utils import keyboard

from data.config import BACK_TO_MAIN_MENU_BUTTON_TEXT


async def send_back_to_main_menu_message(message: types.Message) -> None:
    markup_builder = keyboard.ReplyKeyboardBuilder()
    markup_builder.button(text=BACK_TO_MAIN_MENU_BUTTON_TEXT)
    markup = markup_builder.as_markup(resize_keyboard=True)

    await message.answer(text='🟢', reply_markup=markup)