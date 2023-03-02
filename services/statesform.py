from aiogram.fsm.state import State, StatesGroup


class WriteFuture(StatesGroup):
    transaction_data = State()
    klines_data = State()
    statistics_24hr = State()
    best_price = State()
    choice_future = State()
    notification = State()
