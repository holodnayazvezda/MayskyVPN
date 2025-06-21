from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from data.config import INBOUNDS_DATA
from handlers.bot_info import BotInfo
from handlers.connection.starter import connection_section_starter
from utils.users.users_balance_worker import change_rub_balance, change_star_balance
from utils.users.users_connections_worker import add_user_to_connections_db
from utils.users.users_data import UsersData
from utils.x_ui.config_string import generate_config_string
from utils.x_ui.inbounds_ids_worker import get_inbound_id
from utils.x_ui.user import create_user


async def debit_money(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo) -> None:
    users_data = UsersData(await state.get_data())
    connection_data = users_data.connection_data

    currency = 'rubbles' if call.data.startswith('pay_rubles') else 'stars'
    amount = int(call.data.split(':')[1])

    if currency == 'rubbles':
        change_rub_balance(call.from_user.id, f'-{amount}')
    else:
        change_star_balance(call.from_user.id, f'-{amount}')

    selected_tariff_id = call.data.split('-')[1].split(':')[0]
    amount_of_devices, amount_of_months = map(int, selected_tariff_id.split('_'))

    inbound_id = await get_inbound_id(INBOUNDS_DATA[selected_tariff_id]['remark'])
    expiry_time = (int(datetime.now().timestamp()) + 60 * 60 * 24 * 30 * amount_of_months) * 1000  # формат в милисекундах
    # Считается, что если раньше у пользователя был тариф, то пользователь x-ui с таким же username уже не существует
    # TODO: проверить, что это так и если нет, то удалить пользователя x-ui с таким же username
    user_uuid = await create_user(
        inbound_id, call.from_user.username, call.from_user.id,
        expiry_time=expiry_time, limit_ip=amount_of_devices
    )

    connection_type = INBOUNDS_DATA[selected_tariff_id]["remark"]
    connection_string = await generate_config_string(inbound_id, user_uuid, call.from_user.username)

    connection_data['connection_type'] = connection_type
    connection_data['inbound_id'] = inbound_id
    connection_data['user_uuid'] = user_uuid
    connection_data['expiry_time'] = expiry_time
    connection_data['limit_ip'] = amount_of_devices
    connection_data['key'] = connection_string

    await call.answer(text=f'✅ Оплата прошла успешно! Тариф {INBOUNDS_DATA[selected_tariff_id]["remark"]} подключен.', show_alert=True)

    await state.set_data(users_data.to_dict())
    await connection_section_starter(call.message, state, bot_instance)

    add_user_to_connections_db(
        call.message.chat.id, bot_instance.token, inbound_id, user_uuid, expiry_time,
        connection_type, amount_of_devices, connection_string
    )
