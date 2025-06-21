from aiogram.filters.state import State, StatesGroup

class ConnectionState(StatesGroup):
    has_connection = State()
    have_connection = State()
    does_not_have_connection = State()
    selecting_tariff = State()
    tariff_on_payment = State()
