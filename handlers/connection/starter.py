from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from handlers.bot_info import BotInfo
from handlers.states.connection_state import ConnectionState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.text_workers.timestamp_worker import unix_to_date, calculate_remaining_time, is_expired
from utils.users.trial_users_worker import can_use_trial
from utils.users.users_data import UsersData


async def connection_section_starter(message: types.Message, state: FSMContext, bot_instance: BotInfo):
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data
    connection_data = users_data.connection_data

    # получаем данные подключения пользователя
    message_id = messages_data.get('message_with_markup_id', None)
    if 'inbound_id' in connection_data and 'expiry_time' in connection_data and not is_expired(connection_data['expiry_time']):
        await state.set_state(ConnectionState.has_connection)
        connection_type = connection_data['connection_type']
        expiry_time = connection_data['expiry_time']
        limit_ip = connection_data['limit_ip']
        key = connection_data['key']

        expiry_date = unix_to_date(expiry_time)
        rest_days, rest_hours = calculate_remaining_time(expiry_time)

        current_bot = await bot_instance.bot.get_me()
        message_text = get_text_and_format_it(
            './data/message_texts/connection_section_connection_info.txt',
            key,
            current_bot.username,
            connection_type,
            expiry_date, rest_days, rest_hours,
            limit_ip
        )

        message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                    chat_id=message.chat.id,
                                                    text=message_text,
                                                    message_id=message_id,
                                                    parse_mode=ParseMode.MARKDOWN)
        # получить другие данные подключения (по типу остатку по времени, количество устройств и т.д.) и отобразить
    else:
        await state.set_state(ConnectionState.does_not_have_connection)
        trial_available = await can_use_trial(message.from_user.id)

        if trial_available:
            filename = './data/message_texts/connection_section_no_inbound_can_use_trial.txt'
        else:
            filename = './data/message_texts/connection_section_no_inbound_cannot_use_trial.txt'

        current_bot = await bot_instance.bot.get_me()
        message_text = get_text_and_format_it(filename, message.from_user.first_name, current_bot.username)

        reply_markup_builder = keyboard.InlineKeyboardBuilder()
        if await can_use_trial(message.from_user.id):
            reply_markup_builder.button(text='✅ Подключить пробный период', callback_data='trial')
        reply_markup_builder.button(text='🫵🏻 Выбрать тариф', callback_data='select_tariff')
        reply_markup = reply_markup_builder.as_markup()

        message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                    chat_id=message.chat.id,
                                                    text=message_text,
                                                    message_id=message_id,
                                                    reply_markup=reply_markup,
                                                    parse_mode=ParseMode.MARKDOWN)

    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())
