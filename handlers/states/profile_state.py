from aiogram.filters.state import State, StatesGroup

class ProfileState(StatesGroup):
    start = State()
    price_in_rubles_is_selected = State()
    price_in_stars_is_selected = State()
    on_payment = State()

