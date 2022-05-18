from aiogram.dispatcher.filters.state import StatesGroup, State

class AdvSt(StatesGroup):
    wait_for_adv = State()
    wait_for_screen = State()