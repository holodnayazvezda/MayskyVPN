import asyncio
from datetime import datetime as dt

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard

from handlers.bot_info import BotInfo
from handlers.states.profile_state import ProfileState
from utils.messages.messages_sender import try_edit_or_send_message
from utils.payment.automatic_payment_checker import check_payment_automatically
from utils.payment.yoomoney_api_worker import get_payment_link
from utils.text_workers.get_message_text import get_text_and_format_it
from utils.users.users_data import UsersData


async def send_rubles_invoice(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    await state.set_state(ProfileState.on_payment)

    bot = await bot_instance.bot.get_me()
    message_text = get_text_and_format_it('./data/message_texts/pay_this_bill.txt', bot.username)
    price = int(call.data.split(':')[1])

    order_id = f'{call.from_user.id}-{call.data}-{dt.now()}'

    payment_link = await get_payment_link(order_id, price, message_text)

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text=f'💳 Оплатить {price}₽', url=payment_link)
    markup_builder.button(text='◀️ Назад', callback_data='back_to_choose_sum_in_rub')
    markup_builder.adjust(1)

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

    await asyncio.to_thread(check_payment_automatically, call, bot_instance, order_id, asyncio.get_event_loop())

