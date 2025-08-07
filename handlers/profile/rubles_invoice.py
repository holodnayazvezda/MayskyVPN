from datetime import datetime as dt

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard

from data import PAYMENT_TOKENS
from handlers.bot_info import BotInfo
from handlers.states.profile_state import ProfileState
from utils.users.users_data import UsersData


async def send_rubles_invoice(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    await state.set_state(ProfileState.on_payment)

    bot = await bot_instance.bot.get_me()
    payment_token = PAYMENT_TOKENS[bot.bot.token]
    price = int(call.data.split(':')[1])

    order_id = f'{call.from_user.id}-{call.data}-{dt.now()}'
    prices = [types.LabeledPrice(label=f"Пополнение баланса на {price}₽", amount=price * 100)]

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text=f'Оплатить {price}₽', pay=True)
    markup_builder.button(text='◀️ Назад', callback_data='back_to_choose_sum_in_rub')
    markup_builder.adjust(1)
    markup = markup_builder.as_markup()

    message_id = (await call.message.answer_invoice(
        title=f"Пополнение баланса",
        payload=order_id,
        description=f"Оплатите этот счет, чтобы пополнить баланс в @{bot.username}",
        currency="RUB",
        prices=prices,
        provider_token=payment_token,
        is_flexible=False,
        reply_markup=markup
    )).message_id

    await call.message.delete()
    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())
