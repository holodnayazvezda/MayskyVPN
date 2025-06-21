from aiogram import Bot

from telebot import TeleBot


async def safe_delete_message(bot: Bot, chat_id: int, message_id: int) -> None:
    """
    Deletes a message from the chat using aiogram.
    """
    if not message_id:
        return

    try:
        await bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass


async def safe_delete_messages(bot: Bot, chat_id: int, message_ids: list) -> None:
    if not message_ids:
        return

    for message_id in message_ids:
        await safe_delete_message(bot, chat_id, message_id)


def safe_delete_message_via_telebot(bot_telebot: TeleBot, chat_id: int, message_id: int) -> None:
    """
    Deletes a message from the chat using telebot.
    """
    if message_id:
        try:
            bot_telebot.delete_message(chat_id, message_id)
        except Exception as e:
            pass


