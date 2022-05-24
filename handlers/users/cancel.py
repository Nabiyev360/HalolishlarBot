from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from data.admins_list import ADMINS
from keyboards.default.mainMenu import main_menu
from keyboards.default.adminKeyboards import admin_main



@dp.message_handler(text='❌ Bekor qilish', state='*')
async def cancel_handler(msg: Message, state: FSMContext):
	await msg.answer("❌ Bekor qilindi. Siz asosiy menyudasiz.", reply_markup=main_menu)

	await state.finish()



@dp.message_handler(text=['✖️ Bekor qilish', '/bekor'], state='*')
async def set_handler(msg: Message, state:FSMContext):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		await msg.answer("Bekor qilindi!", reply_markup=admin_main)

		await state.finish()