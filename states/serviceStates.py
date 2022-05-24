from aiogram.dispatcher.filters.state import StatesGroup, State

class SerSt(StatesGroup):
    input_service_name = State()
    input_service_region = State()
    input_service_price = State()
    input_service_contact = State()
    service_confirm_cancel = State()

    input_chek = State()