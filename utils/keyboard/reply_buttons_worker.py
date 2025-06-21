from aiogram.utils import keyboard

def get_reply_buttons_list(buttons_texts: list) -> list:
    return list(map(lambda btn_text: keyboard.KeyboardButton(text=btn_text), buttons_texts))