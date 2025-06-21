from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from data.config import INBOUNDS_DATA
from handlers.bot_info import BotInfo
from handlers.states.connection_state import ConnectionState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.users.users_balance_worker import get_rub_balance, get_star_balance
from utils.users.users_data import UsersData


async def confirm_payment(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    selected_tariff_id = call.data
    selected_tariff_data = INBOUNDS_DATA[selected_tariff_id]
    price_rubles, price_stars = selected_tariff_data['price_rubles'], selected_tariff_data['price_stars']
    balance_rubles, balance_stars = get_rub_balance(call.from_user.id), get_star_balance(call.from_user.id)

    if price_rubles > balance_rubles and price_stars > balance_stars:
        callback_text = get_text_and_format_it(
            './data/message_texts/insufficient_balance.txt',
            price_rubles, price_stars,
            balance_rubles, balance_stars
        )
        await call.answer(callback_text, show_alert=True)
        return

    await state.set_state(ConnectionState.tariff_on_payment)

    reply_markup_builder = keyboard.InlineKeyboardBuilder()
    if price_rubles <= balance_rubles:
        reply_markup_builder.button(text=f'💳 Оплатить {price_rubles} ₽', callback_data=f'pay_rubles-{selected_tariff_id}:{price_rubles}')
    if price_stars <= balance_stars:
        reply_markup_builder.button(text=f'💸 Оплатить {price_stars} ⭐', callback_data=f'pay_stars-{selected_tariff_id}:{price_stars}')
    reply_markup_builder.button(text='◀️ Назад', callback_data='back_to_choosing_tariff')
    reply_markup_builder.adjust(1)
    markup = reply_markup_builder.as_markup()

    message_text = get_text_and_format_it(
        './data/message_texts/confirm_payment.txt',
        selected_tariff_data['remark'],
        price_rubles,
        price_stars
    )

    message_id = messages_data.get('message_with_markup_id', None)
    message_id = await try_edit_or_send_message(
        bot=bot_instance.bot,
        chat_id=call.message.chat.id,
        text=message_text,
        message_id=message_id,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())
