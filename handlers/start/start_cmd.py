from aiogram import types
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from data.config import START_BUTTONS, STARS_FOR_REFERRAL
from handlers.back_to_main_menu_message import send_back_to_main_menu_message
from handlers.bot_info import BotInfo
from handlers.connection.starter import connection_section_starter
from handlers.manual.starter import manual_section_starter
from handlers.profile.starter import profile_section_starter
from handlers.states.start_state import StartState
from utils.keyboard.reply_buttons_worker import get_reply_buttons_list
from utils.messages.messages_deleter import safe_delete_message
from utils.messages.messages_sender import send_message
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.users.referral_users_worker import register_user
from utils.users.users_balance_worker import change_star_balance
from utils.users.users_data import UsersData


async def start_cmd_processor(
    message: types.Message,
    state: FSMContext,
    bot_instance: BotInfo,
    check_command_args: bool,
) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    if check_command_args:
        data = message.text.split()[1]
        if data == 'connection':
            await message.delete()
            await connection_section_starter(message, state, bot_instance)
            return
        elif data == 'profile':
            await message.delete()
            await profile_section_starter(message, state, bot_instance)
            return
        elif data == 'manual':
            await message.delete()
            await manual_section_starter(message, state, bot_instance)
            return
        else:
            user_id, referrer_id = message.from_user.id, int(data)
            res = register_user(user_id, referrer_id)
            if res:
                change_star_balance(referrer_id, f'+{STARS_FOR_REFERRAL}')

    if 'message_with_markup_id' in messages_data:
        await safe_delete_message(bot_instance.bot, chat_id=message.chat.id, message_id=messages_data['message_with_markup_id'])


    await state.set_state(StartState.start)

    markup_builder = keyboard.ReplyKeyboardBuilder()
    markup_builder.add(*get_reply_buttons_list(START_BUTTONS))
    markup_builder.adjust(1)
    markup = markup_builder.as_markup(resize_keyboard=True)


    message_text = get_text_and_format_it('./data/message_texts/welcome.txt', message.from_user.first_name)

    await send_message(
        bot=bot_instance.bot,
        chat_id=message.chat.id,
        text=message_text,
        reply_markup=markup,
        parse_mode="markdown"
    )


    messages_data['message_with_markup_id'] = None
    await state.set_data(users_data.to_dict())
    # регистрируем
    register_user(message.from_user.id)
