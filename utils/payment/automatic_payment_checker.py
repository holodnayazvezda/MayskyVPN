import asyncio
import time

from aiogram import types
from aiogram.fsm.context import FSMContext
from telebot import types as tb_types

from handlers.bot_info import BotInfo
from utils.messages.messages_sender import try_edit_or_send_message_via_telebot
from utils.payment.yoomoney_api_worker import check_payment
from utils.users.users_balance_worker import change_rub_balance


def check_payment_automatically(
        call: types.CallbackQuery, bot_instance: BotInfo,
        order_id: str, event_loop
) -> None:
    for _ in range(60):
        is_paid = asyncio.run_coroutine_threadsafe(check_payment(order_id), event_loop).result()
        if is_paid:
            price = int(order_id.split('-')[1].split(':')[1])
            change_rub_balance(call.from_user.id, f'+{price}')

            message_text = f'✅ Оплата прошла успешно! На ваш баланс зачислено *{price}₽*'
            markup = tb_types.InlineKeyboardMarkup()
            markup.add(tb_types.InlineKeyboardButton(text='⏪ Назад в личный кабинет', callback_data='back_to_start'))
            try_edit_or_send_message_via_telebot(
                bot_telebot=bot_instance.bot_telebot,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=message_text,
                reply_markup=markup,
                parse_mode='markdown'
            )
            break
        time.sleep(10)

    else:
        message_text = '❗️ Время на оплату счета истекло'
        markup = tb_types.InlineKeyboardMarkup()
        markup.add(tb_types.InlineKeyboardButton(
            text='🔄 Обновить счет',
            callback_data='back_to_choose_sum_in_rub'
        ))
        try_edit_or_send_message_via_telebot(
            bot_telebot=bot_instance.bot_telebot,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=message_text,
            reply_markup=markup,
            parse_mode='markdown'
        )