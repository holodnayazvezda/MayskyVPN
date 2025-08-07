from datetime import datetime as dt

from aiogram import types
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from handlers.bot_info import BotInfo
from handlers.states.profile_state import ProfileState
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.users.users_data import UsersData


async def send_stars_invoice(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    await state.set_state(ProfileState.on_payment)

    price = int(call.data.split(':')[1])

    order_id = f'{call.from_user.id}-{call.data}-{dt.now()}'
    prices = [types.LabeledPrice(label="XTR", amount=price)]

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text=f'Оплатить {price} ⭐️', pay=True)
    markup_builder.button(text='◀️ Назад', callback_data='back_to_choose_sum_in_stars')
    markup_builder.adjust(1)
    markup = markup_builder.as_markup()

    message_id = (await call.message.answer_invoice(
        title=f"Пополнение баланса",
        description=f"Оплатите этот счет, чтобы пополнить баланс на {price} ⭐️",
        prices=prices,
        payload=order_id,
        reply_markup=markup,
        currency="XTR"
    )).message_id

    await call.message.delete()
    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())
