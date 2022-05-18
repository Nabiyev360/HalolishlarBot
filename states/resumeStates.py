from aiogram.dispatcher.filters.state import StatesGroup, State

class ResSt(StatesGroup):
    input_name = State()
    input_birth = State()
    input_region = State()
    input_position = State()
    input_contact = State()
    input_salary = State()
    input_contact = State()
    input_experience = State()
    input_education = State()
    input_skills = State()
    input_recommend = State()
    input_additional = State()
    input_portfolio = State()
    confirm_cancel = State()