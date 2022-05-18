from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from pyqiwip2p import QiwiP2P
from random import randint

from loader import dp, db
from data.config import ADMINS
from keyboards.inline.advKeyboards import check_pay, price_buttons
from keyboards.default.mainMenu import main_menu
from keyboards.default.buttons import cancel_btn
from states.advStates import AdvSt



@dp.message_handler(text = '💸 Reklama joylashtirish')
async def advert_handler(msg: Message):
	tarif1, tarif2, tarif3, price1, price2, price3 = db.get_adv_prices()
	await msg.answer(
		text = f"Kanalda reklama joylashtirish tariflari: 👇\n\n{tarif1} - {price1} rub.\n{tarif2} - {price2} rub.\n{tarif3} - {price3} rub.\n\nO'zingizga qulay tarifni tanlang", 
		reply_markup = price_buttons(tarif1, tarif2, tarif3, price1 +' rub.', price2 +' rub.', price3 +' rub.'))


@dp.callback_query_handler(text_contains = 'adv-tarif')
async def tarif_handler(call: CallbackQuery, state: FSMContext):
	tarif_num = call.data[-1]
	tarif1, tarif2, tarif3, price1, price2, price3 = db.get_adv_prices()
	
	choosed_tarif = ''

	if tarif_num == '1':
		await state.update_data({'price': price1})
		choosed_tarif = tarif1
		choosed_price = price1
	elif tarif_num == '2':
		await state.update_data({'price': price2})
		choosed_tarif = tarif2
		choosed_price = price2
	elif tarif_num == '3':
		await state.update_data({'price': price3})		
		choosed_tarif = tarif3
		choosed_price = price3

	QIWI_TOKEN =  db.get_one('qiwi_wallet')
	p2p = QiwiP2P(auth_key=QIWI_TOKEN)
	comment = str(call.from_user.id) + '_' + call.from_user.full_name + '_' + str(randint(1, 9999))

	bill = p2p.bill(amount=int(choosed_price), lifetime=10, comment=comment)

	text = f"Siz <b>{choosed_tarif}</b> tarifni tanladingiz. To'lovni amalga oshirganingizdan so'ng reklamani yuborishingiz mumkin."
	await call.message.edit_text(text=text, reply_markup=check_pay(bill.pay_url, bill.bill_id, choosed_price))


@dp.callback_query_handler(text_contains = 'check-')
async def check_handler(call: CallbackQuery):
	QIWI_TOKEN =  db.get_one('qiwi_wallet')
	p2p = QiwiP2P(auth_key=QIWI_TOKEN)
	bill = str(call.data[6:])
	status = str(p2p.check(bill_id=bill).status)
	if status == "PAID":
		await call.message.answer("✅ To'lov amalga oshirildi! Reklamangizni yuboring", reply_markup=cancel_btn)
		await AdvSt.wait_for_adv.set()

	elif status == "WAITING":
		await call.answer("⏳ To'lov amalga oshirilishi kutilmoqda...", show_alert=True)
	else:
		await call.answer("❌ To'lov amalga oshirilmadi!", show_alert=True)
		await call.message.delete()



@dp.callback_query_handler(text_contains = 'uzcard-humo-')
async def uzpay_handler(call: CallbackQuery):
	uzcard_num = db.get_one('uzcard_num')
	summa = call.data[12:]
	text = f"Quyidagi hisobga {summa} rubl o'tkazib, chek rasmini (skrinshotni) yuboring...\n\n💳KARTA RAQAM: <code>{uzcard_num}</code>"
	
	await call.message.answer(text=text, reply_markup=cancel_btn)
	await call.message.delete()
	await AdvSt.wait_for_screen.set()



@dp.message_handler(state=AdvSt.wait_for_screen, content_types='any')
async def screen_handler(msg: Message, state:FSMContext):
	await dp.bot.send_message(chat_id=ADMINS[0], text = f"<a href='https://t.me/{msg.from_user.username}'>{msg.from_user.full_name}</a> to'lov cheki yubordi👇", disable_web_page_preview=True)
	await msg.send_copy(chat_id=ADMINS[0])
	await msg.answer("Chek adming yuborildi. Endi reklamangizni yuboring...", reply_markup=cancel_btn)
	await AdvSt.wait_for_adv.set()


@dp.message_handler(state=AdvSt.wait_for_adv, content_types='any')
async def adv_handler(msg: Message, state:FSMContext):
	await dp.bot.send_message(chat_id=ADMINS[0], text = f"<a href='https://t.me/{msg.from_user.username}'>{msg.from_user.full_name}</a> kanalga joylashtirish uchun reklama yubordi👇", disable_web_page_preview=True)
	await msg.send_copy(chat_id=ADMINS[0])
	await msg.answer("✅ Qabul qilindi! Reklamangiz admin tasdig'idan o'tgandan so'ng kanalga joylashiritiladi!",
		reply_markup=main_menu)
	await state.finish()



@dp.callback_query_handler(text = 'cancel')
async def tarif_handler(call: CallbackQuery):
	await call.message.delete()
	await dp.send_message(chat_id=call.from_user.id, text="Asosiy menu", reply_markup=main_menu)