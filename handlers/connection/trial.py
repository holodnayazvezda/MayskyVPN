from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from data import TRIAL_DURATION
from handlers.bot_info import BotInfo
from handlers.connection.starter import connection_section_starter
from utils.users.trial_users_worker import remember_users_trial
from utils.users.users_connections_worker import add_user_to_connections_db
from utils.users.users_data import UsersData
from utils.x_ui.config_string import generate_config_string
from utils.x_ui.inbounds_ids_worker import get_inbound_id
from utils.x_ui.user import create_user


async def generate_trial_config(call: types.CallbackQuery, state: FSMContext, bot_instance: BotInfo):
    users_data = UsersData(await state.get_data())
    connection_data = users_data.connection_data

    trial_inbound_id = await get_inbound_id('Пробный период')
    expiry_time = (int(datetime.now().timestamp()) + 60 * 60 * 24 * TRIAL_DURATION) * 1000  # формат в милисекундах
    user_uuid = await create_user(
        trial_inbound_id, call.from_user.username, call.from_user.id,
        expiry_time=expiry_time, limit_ip=1
    )

    connection_type = 'Пробный период'
    connection_string = await generate_config_string(trial_inbound_id, user_uuid, call.from_user.username)

    connection_data['connection_type'] = connection_type
    connection_data['inbound_id'] = trial_inbound_id
    connection_data['user_uuid'] = user_uuid
    connection_data['expiry_time'] = expiry_time
    connection_data['limit_ip'] = 1
    connection_data['key'] = connection_string

    await call.answer('✅ Пробный период подключен!', show_alert=True)

    await state.set_data(users_data.to_dict())
    await connection_section_starter(call.message, state, bot_instance)

    await remember_users_trial(call.from_user.id)

    add_user_to_connections_db(
        call.message.chat.id, bot_instance.token, trial_inbound_id, user_uuid, expiry_time,
        connection_type, 1, connection_string
    )
