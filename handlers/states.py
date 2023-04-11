from aiogram.dispatcher.filters.state import State, StatesGroup


class addRess(StatesGroup):
    msg0 = State()
    st = State()

class post(StatesGroup):
    msg0 = State()
    media = State()
    text = State()
    kb = State()
    settigs = State()