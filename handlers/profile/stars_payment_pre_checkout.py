from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery

from utils.users.users_balance_worker import change_star_balance
from utils.users.users_data import UsersData


async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    price = pre_checkout_query.total_amount
    change_star_balance(pre_checkout_query.from_user.id, f'+{price}')

    await pre_checkout_query.answer(ok=True)