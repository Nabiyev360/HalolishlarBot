from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from pyqiwip2p import QiwiP2P

from loader import dp, db
from keyboards.default.buttons import cancel_btn, confrim_btn
from keyboards.default.mainMenu import main_menu
from keyboards.inline.confirmAdmin import confirm_admin
from keyboards.inline.advKeyboards import check_pay

from states.vacancyStates import VacSt
from states.advStates import AdvSt
from states.resumeStates import ResSt
from states.serviceStates import SerSt

@dp.callback_query_handler(text_contains = 'uzcard-humo-')
async def uzpay_handler(call: CallbackQuery):
	uzcard_num = db.get_one('uzcard_num')
	summa = call.data[12:]
	text = f"Quyidagi hisobga {summa} so'm o'tkazib, chek rasmini (skrinshotni) yuboring...\n\n💳KARTA RAQAM: <code>{uzcard_num}</code>"
	
	if 'reklamani' in call.message.text:
		await AdvSt.wait_for_screen.set()
	elif 'vakansiya' in call.message.text:
		await VacSt.input_chek.set()
	elif 'xizmat' in call.message.text:
		await SerSt.input_chek.set()
	elif 'rezyume' in call.message.text:
		await ResSt.input_chek.set()

	await call.message.answer(text=text, reply_markup=cancel_btn)
	await call.message.delete()



@dp.callback_query_handler(text_contains = 'check-')
async def check_handler(call: CallbackQuery):
	QIWI_TOKEN =  db.get_one('qiwi_wallet')
	p2p = QiwiP2P(auth_key=QIWI_TOKEN)
	bill = str(call.data[10:])
	category = str(call.data[:3])

	status = str(p2p.check(bill_id=bill).status)
	if status == "PAID":
		if category == 'adv':
			text = "✅ To'lov amalga oshirildi! Reklamangizni yuboring"
			await AdvSt.wait_for_adv.set()
		
		elif category == 'vac':
			text = "1. Lavozim nomini kiriting.\n\nMisol: Kopirayter, Dasturchi, Dizayner, Savdo menejeri."
			await VacSt.input_position.set()
		
		elif category == 'res':
			text = "1. Familiya, ism va sharfingizni kiriting."
			await ResSt.input_name.set()

		elif category == 'ser':
			text = "1. Xizmat turini kiriting.\n\nMisol: Yuk tashish, Enagalik xizmati, Shaxsiy o'qituvchi"
			await SerSt.input_service_name.set()

		await call.message.answer(text, reply_markup=cancel_btn)
		await call.message.delete()


	elif status == "WAITING":
		await call.answer("⏳ To'lov amalga oshirilishi kutilmoqda...", show_alert=True)
	else:
		await call.answer("❌ To'lov amalga oshirilmadi!", show_alert=True)
		await call.message.delete()