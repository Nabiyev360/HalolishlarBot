from aiogram.dispatcher.filters.state import StatesGroup, State

class VacSt(StatesGroup):
    input_position = State()
    input_company = State()
    input_duties = State()
    input_important = State()
    input_conditions = State()
    input_salary = State()
    input_contact = State()
    confirm_cancel = State()

    input_chek = State()