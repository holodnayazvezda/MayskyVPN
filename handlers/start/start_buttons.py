from aiogram import types
from aiogram.fsm.context import FSMContext

from data.config import BACK_TO_MAIN_MENU_BUTTON_TEXT, START_BUTTONS
from handlers.manual.starter import manual_section_starter
from handlers.profile.starter import profile_section_starter
from handlers.back_to_main_menu_message import send_back_to_main_menu_message
from handlers.bot_info import BotInfo
from handlers.connection.starter import connection_section_starter


async def process_start_buttons(
    message: types.Message,
    state: FSMContext,
    bot_instance: BotInfo
) -> None:
    if message.text == START_BUTTONS[0]:
        await send_back_to_main_menu_message(message)
        await connection_section_starter(message, state, bot_instance)
    elif message.text == START_BUTTONS[1]:
        await send_back_to_main_menu_message(message)
        await profile_section_starter(message, state, bot_instance)
    elif message.text == START_BUTTONS[2]:
        await send_back_to_main_menu_message(message)
        await manual_section_starter(message, state, bot_instance)
