from aiogram.dispatcher.filters.state import StatesGroup, State

class SetSt(StatesGroup):
    wait_ann_price = State()
    wait_ann_price_uzs = State()
    wait_adv_value = State()
    wait_qiwi_token = State()
    wait_uzcard_num = State()
    wait_interval = State()
    wait_admin_id = State()
    waiting_admin_message = State()