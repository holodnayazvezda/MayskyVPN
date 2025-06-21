from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from data.config import INBOUNDS_DATA
from handlers.bot_info import BotInfo
from handlers.states.connection_state import ConnectionState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.text_workers import get_text_and_format_it
from utils.users.users_data import UsersData


async def choose_tariff(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    await state.set_state(ConnectionState.selecting_tariff)

    reply_markup_builder = keyboard.InlineKeyboardBuilder()
    for tariff_id in list(INBOUNDS_DATA.keys()):
        reply_markup_builder.button(text=INBOUNDS_DATA[tariff_id]['remark'], callback_data=tariff_id)
    reply_markup_builder.button(text='◀️ Назад', callback_data='back_to_connection_starter')
    reply_markup_builder.adjust(3)
    markup = reply_markup_builder.as_markup()

    message_id = messages_data.get('message_with_markup_id', None)
    current_bot = await bot_instance.bot.get_me()
    message_text = get_text_and_format_it(
        './data/message_texts/choose_tariff.txt',
        current_bot.username
    )

    message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                    chat_id=call.message.chat.id,
                                                    text=message_text,
                                                    message_id=message_id,
                                                    reply_markup=markup,
                                                    parse_mode=ParseMode.MARKDOWN)
    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())

