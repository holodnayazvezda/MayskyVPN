from typing import Union

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard

from handlers.bot_info import BotInfo
from handlers.states.manual_state import ManualState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.users.users_data import UsersData


async def manual_section_starter(
        call_or_message: Union[types.Message, types.CallbackQuery],
        state: FSMContext, bot_instance: BotInfo
):
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    await state.set_state(ManualState.start)

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text='📱 IOS / iPadOS / 💻 MacOS', callback_data='apple')
    markup_builder.button(text='🤖 Android', callback_data='android')
    markup_builder.button(text='🖥 Windows', callback_data='windows')
    markup_builder.adjust(1)
    markup = markup_builder.as_markup()

    message_id = messages_data.get('message_with_markup_id', None)
    chat_id = call_or_message.chat.id if isinstance(call_or_message, types.Message) else call_or_message.message.chat.id

    message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                chat_id=chat_id,
                                                text='💾 Выберите операционную систему для получения инструкций:',
                                                message_id=message_id,
                                                reply_markup=markup)

    messages_data['message_with_markup_id'] = message_id
    await state.update_data(messages_data=messages_data)
