from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, types
from aiogram.types import FSInputFile

from telebot import TeleBot, types as tb_types

from utils.files.remover import safe_remove_files
from utils.messages.messages_deleter import safe_delete_message, safe_delete_message_via_telebot, safe_delete_messages


def cut_the_message_text(message_text):
    if len(message_text) >= 4096:
        return message_text[:4092] + '...'
    return message_text


async def try_edit_or_send_message(bot: Bot, chat_id: int, text: str, message_id: int = None,
                                   reply_markup = None, parse_mode: str = None,
                                   photos_to_delete_ids: list[int] = []) -> int:
    await safe_delete_messages(bot, chat_id, photos_to_delete_ids)
    try:
        if message_id:
            x = await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=cut_the_message_text(text),
                                            reply_markup=reply_markup, parse_mode=parse_mode,
                                            disable_web_page_preview=True)
        else:
            x = await bot.send_message(chat_id=chat_id, text=cut_the_message_text(text), reply_markup=reply_markup,
                                       parse_mode = parse_mode, disable_web_page_preview=True)
        return x.message_id
    except Exception as e:
        if "can't parse entities" in str(e).lower():
            return await try_edit_or_send_message(bot, chat_id, text, message_id, reply_markup, None)
        try:
            await safe_delete_message(bot, chat_id, message_id)
            x = await bot.send_message(chat_id=chat_id, text=cut_the_message_text(text), reply_markup=reply_markup,
                                       parse_mode=parse_mode, disable_web_page_preview=True)
            return x.message_id
        except Exception:
            pass


async def send_message(bot: Bot, chat_id: int, text: str, message_id: int = None,
                       reply_markup = None, parse_mode: str = None,
                       photos_to_delete_ids: list[int] = []) -> int:
    await safe_delete_messages(bot, chat_id, photos_to_delete_ids)
    await safe_delete_message(bot, chat_id, message_id)
    try:
        x = await bot.send_message(chat_id=chat_id, text=cut_the_message_text(text), reply_markup=reply_markup,
                                   parse_mode=parse_mode, disable_web_page_preview=True)
        return x.message_id
    except TelegramBadRequest as e:
        if "can't parse entities" in str(e).lower():
            return await send_message(bot, chat_id, text, message_id, reply_markup, None)


async def send_photo(bot: Bot, chat_id: int, photo: bytes, caption: str = None,
                     message_id: int = None, reply_markup = None, parse_mode: str = None) -> int:
    await safe_delete_message(bot, chat_id, message_id)
    try:
        x = await bot.send_photo(chat_id=chat_id, photo=types.BufferedInputFile(photo, 'book_cover.jpg'),
                                 caption=caption, reply_markup=reply_markup, parse_mode=parse_mode)
        return x.message_id
    except TelegramBadRequest as e:
        if "can't parse entities" in str(e).lower():
            return await send_photo(bot, chat_id, photo, caption, message_id, reply_markup, None)


async def send_media_group(bot: Bot, chat_id: int, photos_urls: list[str], message_id: int = None,
                           photos_to_delete_ids: list[int] = []) -> list[int]:
    await safe_delete_messages(bot, chat_id, photos_to_delete_ids)
    await safe_delete_message(bot, chat_id, message_id)
    input_media_photos = list(map(
        lambda image_link: types.InputMediaPhoto(media=image_link, parse_mode='html'),
        photos_urls)
    )
    try:
        send_photos_messages_objects = await bot.send_media_group(chat_id=chat_id, media=input_media_photos)
        send_photos_ids = list(map(lambda message: message.message_id, send_photos_messages_objects))
        return send_photos_ids
    except Exception:
        pass


async def send_document(bot: Bot, chat_id: int, filepath: str, filename: str = None, caption: str = None,
                        message_id: int = None, reply_markup=None, parse_mode: str = None) -> int:
    await safe_delete_message(bot, chat_id, message_id)
    try:
        x = await bot.send_document(
            chat_id=chat_id, document=FSInputFile(path=filepath, filename=filename),
            caption=caption, reply_markup=reply_markup, parse_mode=parse_mode
        )

        safe_remove_files(filepath)

        return x.message_id
    except TelegramBadRequest:
        pass



def send_message_via_telebot(bot_telebot: TeleBot, chat_id: int, text: str, message_id: int = None,
                             reply_markup = None, parse_mode: str = None, reply_to_message_id: int = None) -> int:
    safe_delete_message_via_telebot(bot_telebot, chat_id, message_id)
    try:
        x = bot_telebot.send_message(
            chat_id=chat_id, text=cut_the_message_text(text),
            reply_markup=reply_markup, parse_mode=parse_mode,
            reply_parameters=tb_types.ReplyParameters(message_id=reply_to_message_id) if reply_to_message_id else None,
            disable_web_page_preview=True
        )
        return x.message_id
    except Exception as e:
        if "find end of the entity" in str(e).lower():
            return send_message_via_telebot(bot_telebot, chat_id, text, message_id, reply_markup, None)
        if 'field "message_id" must be' in str(e).lower():
            return send_message_via_telebot(bot_telebot, chat_id, text, message_id, reply_markup, parse_mode, None)


def try_edit_or_send_message_via_telebot(bot_telebot: TeleBot, chat_id: int, text: str, message_id: int = None,
                                         reply_markup=None, parse_mode: str = None) -> int:
    try:
        if message_id is None:
            return send_message_via_telebot(bot_telebot, chat_id, text, message_id, reply_markup, parse_mode)

        x = bot_telebot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup,
                                          parse_mode=parse_mode)
        return x.message_id
    except Exception as e:
        if "find end of the entity" in str(e).lower():
            return try_edit_or_send_message_via_telebot(bot_telebot, chat_id, text, message_id, reply_markup, None)
        else:
            return send_message_via_telebot(bot_telebot, chat_id, text, message_id, reply_markup, parse_mode)


async def answer_callback_query(call: types.CallbackQuery, bot: Bot, text: str = None,
                                show_alert: bool = False) -> None:
    try:
        await bot.answer_callback_query(callback_query_id=call.id, text=text, show_alert=show_alert)
    except Exception:
        pass
