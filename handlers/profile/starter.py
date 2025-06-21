from typing import Union

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from handlers.bot_info import BotInfo
from handlers.states.profile_state import ProfileState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.users.referral_users_worker import get_referred_count
from utils.users.users_balance_worker import get_star_balance, get_rub_balance
from utils.users.users_data import UsersData
from data.config import STARS_FOR_REFERRAL as rate


async def profile_section_starter(
        call_or_message: Union[types.Message, types.CallbackQuery],
        state: FSMContext, bot_instance: BotInfo
):
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data
    connection_data = users_data.connection_data

    await state.set_state(ProfileState.start)

    connection_type = connection_data.get('connection_type', 'Не подключена')
    balance_rubles = get_rub_balance(call_or_message.from_user.id)
    balance_stars = get_star_balance(call_or_message.from_user.id)

    amount_of_referrals = get_referred_count(call_or_message.from_user.id)
    earned_on_referrals = amount_of_referrals * rate

    current_bot = await bot_instance.bot.get_me()
    message_text = get_text_and_format_it(
        './data/message_texts/profile.txt',
        call_or_message.from_user.full_name,
        connection_type,
        balance_rubles, balance_stars,
        amount_of_referrals,
        earned_on_referrals, rate,
        current_bot.username, call_or_message.from_user.id
    )
    message_id = messages_data.get('message_with_markup_id', None)

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text='Пополнить баланс ₽', callback_data='top_up_rub')
    markup_builder.button(text='Пополнить баланс ⭐️', callback_data='top_up_stars')
    markup = markup_builder.as_markup()

    chat_id = call_or_message.chat.id if isinstance(call_or_message, types.Message) else call_or_message.message.chat.id

    message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                chat_id=chat_id,
                                                text=message_text,
                                                message_id=message_id,
                                                reply_markup=markup,
                                                parse_mode=ParseMode.MARKDOWN)

    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())
