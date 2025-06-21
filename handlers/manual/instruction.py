from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard
from aiogram.enums.parse_mode import ParseMode

from handlers.bot_info import BotInfo
from utils.messages.messages_sender import try_edit_or_send_message
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.users.users_data import UsersData


async def send_instruction_for_selected_os(
        call: types.CallbackQuery,
        state: FSMContext,
        bot_instance: BotInfo
) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    if call.data == 'apple':
        message_text_filename = './data/message_texts/manuals/iphone-ipad-macos.txt'
    elif call.data == 'android':
        message_text_filename = './data/message_texts/manuals/android.txt'
    else:
        message_text_filename = './data/message_texts/manuals/windows.txt'

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text='◀️ Назад', callback_data='manual_section_starter')
    markup = markup_builder.as_markup()

    current_bot = await bot_instance.bot.get_me()
    bot_username = current_bot.username
    message_text = get_text_and_format_it(
        message_text_filename,
        str(call.data),
        bot_username,
        bot_username
    )
    message_id = messages_data.get('message_with_markup_id', None)

    message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                chat_id=call.message.chat.id,
                                                text=message_text,
                                                message_id=message_id,
                                                reply_markup=markup,
                                                parse_mode=ParseMode.MARKDOWN)

    messages_data['message_with_markup_id'] = message_id
    await state.update_data(messages_data=messages_data)