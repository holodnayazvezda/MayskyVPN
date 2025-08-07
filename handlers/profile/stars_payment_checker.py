from aiogram import types
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from utils.messages.messages_sender import try_edit_or_send_message
from utils.users import change_rub_balance, change_star_balance
from utils.users.users_data import UsersData


async def success_payment_completed(message: types.Message, state: FSMContext):
    users_data = UsersData(await state.get_data())
    messages_data = users_data.messages_data

    payment_data = message.successful_payment
    if payment_data.currency == 'RUB':
        price = payment_data.total_amount // 100
        payment_amount = f'{price}₽'
        change_rub_balance(message.from_user.id, f'+{price}')   # потому что в копейках
    else:
        price = payment_data.total_amount
        payment_amount = f'{price} ⭐️'
        change_star_balance(message.from_user.id, f'+{price}')

    markup_builder = keyboard.InlineKeyboardBuilder()
    markup_builder.button(text='⏪ Назад в личный кабинет', callback_data='back_to_start')
    markup = markup_builder.as_markup()

    message_id = messages_data.get('message_with_markup_id', None)
    message_id = await try_edit_or_send_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text=f'✅ Оплата прошла успешно! {payment_amount} зачислены на ваш баланс',
        message_id=message_id,
        reply_markup=markup,
        parse_mode='markdown'
    )

    messages_data['message_with_markup_id'] = message_id
    await state.set_data(users_data.to_dict())




