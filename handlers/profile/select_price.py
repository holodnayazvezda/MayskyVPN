from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from data.config import PRICES_IN_RUBLES, PRICES_IN_STARS
from handlers.bot_info import BotInfo
from handlers.states.profile_state import ProfileState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.text_workers import get_text_and_format_it
from utils.users.users_data import UsersData


async def choose_sum_of_payment(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    currency = 'rub' if 'rub' in call.data else 'stars'

    if currency == 'rub':
        await state.set_state(ProfileState.price_in_rubles_is_selected)
        suffix = '₽'
        callback_data_prefix = 'top_up_in_rubles:'
        message_text = get_text_and_format_it('./data/message_texts/select_price_in_rubbles.txt', suffix)
        prices_dataset = PRICES_IN_RUBLES
    else:
        await state.set_state(ProfileState.price_in_stars_is_selected)
        suffix = '⭐️'
        callback_data_prefix = 'top_up_in_stars:'
        message_text = get_text_and_format_it('./data/message_texts/select_price_in_stars.txt', suffix)
        prices_dataset = PRICES_IN_STARS


    markup_builder = keyboard.InlineKeyboardBuilder()
    for price in prices_dataset:
        markup_builder.button(
            text=f'{price}{suffix}',
            callback_data=f'{callback_data_prefix}{price}'
        )
    markup_builder.adjust(4)
    markup_builder.row(types.InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_start'))
    markup = markup_builder.as_markup()

    message_id = messages_data.get('message_with_markup_id', None)
    message_id = await try_edit_or_send_message(bot=bot_instance.bot,
                                                chat_id=call.message.chat.id,
                                                text=message_text,
                                                message_id=message_id,
                                                reply_markup=markup,
                                                parse_mode=ParseMode.MARKDOWN)

    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())