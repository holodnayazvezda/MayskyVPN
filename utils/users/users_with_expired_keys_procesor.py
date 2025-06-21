from telebot import TeleBot
from telebot import types

from utils.text_workers.get_message_text import get_text_and_format_it
from utils.x_ui.user import delete_user


def process_users_with_expired_keys(users_data: list) -> None:
    for user_data in users_data:
        chat_id, bot_token, inbound_id, client_id = user_data
        telebot = TeleBot(token=bot_token)

        bot_username = telebot.get_me().username
        message_text = get_text_and_format_it('./data/message_texts/subscription_expired.txt', bot_username, bot_username)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text='💸 Пополнить баланс', callback_data='back_to_start'))
        markup.add(types.InlineKeyboardButton(text='🫵🏻 Выбрать тариф', callback_data='back_to_choosing_tariff'))

        telebot.send_message(chat_id=chat_id, text=message_text, reply_markup=markup, parse_mode='Markdown')

        delete_user(inbound_id, client_id)
