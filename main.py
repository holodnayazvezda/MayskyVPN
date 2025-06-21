import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
from telebot import TeleBot

from data.config import *
from data.constants import INBOUNDS_DB_PATH
from data.databases_initiator import init_databases
from handlers.bot_info import BotInfo
from handlers.connection.confirm_payment import confirm_payment
from handlers.connection.make_payment_and_generate_config import debit_money
from handlers.connection.starter import connection_section_starter
from handlers.connection.tariff_chooser import choose_tariff
from handlers.connection.trial import generate_trial_config
from handlers.manual.instruction import send_instruction_for_selected_os
from handlers.manual.starter import manual_section_starter
from handlers.profile.rubles_invoice import send_rubles_invoice
from handlers.profile.select_price import choose_sum_of_payment
from handlers.profile.stars_invoice import send_stars_invoice
from handlers.profile.stars_payment_checker import stars_success_payment_completed
from handlers.profile.stars_payment_pre_checkout import pre_checkout_handler
from handlers.profile.starter import profile_section_starter
from handlers.start.start_buttons import process_start_buttons
from handlers.start.start_cmd import start_cmd_processor
from handlers.states.connection_state import ConnectionState
from handlers.states.manual_state import ManualState
from handlers.states.profile_state import ProfileState
from handlers.states.start_state import StartState
from utils.middleware.throttling_call_middleware import ThrottlingCallMiddleware
from utils.middleware.throttling_message_middleware import ThrottlingMessageMiddleware
from utils.users.users_connections_worker import remove_expired_users
from utils.x_ui.inbounds_generator import check_inbounds_table_exists


async def bot_init(token: str) -> None:
    # Cоздаем объект dispatcher для бота, с переданным токеном и настраивает для него middleware.
    dp = Dispatcher(storage=AIOGRAM_REDIS_STORAGE)
    dp.message.middleware(ThrottlingMessageMiddleware(AIOGRAM_REDIS_STORAGE))
    dp.callback_query.middleware(ThrottlingCallMiddleware(AIOGRAM_REDIS_STORAGE))

    # Создаем необходимые объекты ботов, используя переданный токен и формируем объект bot_instance
    bot = Bot(token=token)
    bot_telebot = TeleBot(token=token)
    bot_id = int(token.split(':')[0])
    bot_instance = BotInfo(bot=bot, bot_telebot=bot_telebot, bot_id=bot_id, token=token)

    @dp.message(CommandStart())
    @dp.message(F.text == BACK_TO_MAIN_MENU_BUTTON_TEXT)
    async def start_cmd_handler(message: types.Message, state: FSMContext) -> None:
        await start_cmd_processor(
            message, state, bot_instance,
            message.text != BACK_TO_MAIN_MENU_BUTTON_TEXT and message.text != '/start'
        )

    @dp.message(F.text, StartState.start)
    async def start_buttons_handler(message: types.Message, state: FSMContext) -> None:
        await process_start_buttons(message, state, bot_instance)

    @dp.callback_query(ConnectionState.does_not_have_connection)
    @dp.callback_query(F.data == 'back_to_choosing_tariff')
    async def start_trial_button_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        if call.data == 'trial':
            await generate_trial_config(call, state, bot_instance)
        else:
            await choose_tariff(call, state, bot_instance)

    @dp.callback_query(F.data == 'back_to_connection_starter')
    async def back_to_connection_starter_button_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await connection_section_starter(call.message, state, bot_instance)

    @dp.callback_query(ConnectionState.selecting_tariff)
    async def choose_tariff_buttons_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await confirm_payment(call, state, bot_instance)

    @dp.callback_query(ConnectionState.tariff_on_payment)
    async def confirm_payment_buttons_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await debit_money(call, state, bot_instance)

    @dp.callback_query(ProfileState.start)
    async def top_up_balance_buttons_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await choose_sum_of_payment(call, state, bot_instance)

    @dp.callback_query(F.data == 'back_to_start')
    async def back_to_profile_section_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await profile_section_starter(call, state, bot_instance)

    @dp.callback_query(F.data == 'back_to_choose_sum_in_rub')
    @dp.callback_query(F.data == 'back_to_choose_sum_in_stars')
    async def back_to_choose_sum_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await choose_sum_of_payment(call, state, bot_instance)

    @dp.callback_query(ProfileState.price_in_rubles_is_selected)
    async def sum_in_rubbles_selection_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await send_rubles_invoice(call, state, bot_instance)

    @dp.callback_query(ProfileState.price_in_stars_is_selected)
    async def sum_in_stars_selection_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await send_stars_invoice(call, state, bot_instance)

    @dp.message(F.successful_payment)
    async def successful_payment_handler(message: types.Message, state: FSMContext) -> None:
       await stars_success_payment_completed(message, state)

    @dp.callback_query(F.data == 'manual_section_starter')
    async def back_to_manual_starter_button_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await manual_section_starter(call, state, bot_instance)

    @dp.callback_query(ManualState.start)
    async def choose_os_buttons_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await send_instruction_for_selected_os(call, state, bot_instance)


    dp.pre_checkout_query.register(pre_checkout_handler)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



async def main():
    """
    Получает токены ботов и вызывает функцию, запускающую обработку событий для бота.
    """
    print(f'{len(TOKENS)} bot(s) connected to DanyVPN engine')
    tasks = []
    for token in TEST_TOKENS:
        task = asyncio.create_task(bot_init(token))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_databases()

    scheduler = BackgroundScheduler()
    try:
        scheduler.add_job(remove_expired_users, 'interval', hours=2)
        scheduler.start()

        asyncio.run(check_inbounds_table_exists(INBOUNDS_DB_PATH))
        asyncio.run(main())
    except KeyboardInterrupt:
        scheduler.shutdown()
