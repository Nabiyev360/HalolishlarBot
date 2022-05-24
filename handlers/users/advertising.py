import asyncio
from datetime import datetime
from pyqiwip2p import QiwiP2P
from random import randint
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.admins_list import ADMINS
from keyboards.inline.advKeyboards import check_pay, price_buttons
from keyboards.default.mainMenu import main_menu
from keyboards.default.buttons import cancel_btn
from keyboards.inline.confirmAdmin import confirm_admin
from states.advStates import AdvSt



@dp.message_handler(text = '💸 Reklama joylashtirish')
async def advert_handler(msg: Message):
	res = db.check_interval(msg.from_user.id)
	if res == True:
		tarif1, tarif2, tarif3, price1, price2, price3, price1uzs, price2uzs, price3uzs = db.get_adv_prices()
		await msg.answer(text = f"Kanalda reklama joylashtirish tariflari: 👇\n\n{tarif1} - {price1uzs} so'm | {price1} rub.\n{tarif2} - {price2uzs} so'm | {price2} rub.\n{tarif3} - {price3uzs} so'm | {price3} rub.\n\nO'zingizga qulay tarifni tanlang", 
			reply_markup = price_buttons(tarif1, tarif2, tarif3, price1uzs +" so'm", price2uzs +" so'm", price3uzs +" so'm"))
	else:
		interval, left_days = res
		await msg.answer(f"Kanalga e'lon joylashtirish vaqti oralig'i {interval} kun. \nSiz {left_days} kundan so'ng yana e'lon joylashtirishingiz mumkin 💁‍♂️")


@dp.callback_query_handler(text_contains = 'adv-tarif')
async def tarif_handler(call: CallbackQuery, state: FSMContext):
	tarif_num = call.data[-1]
	tarif1, tarif2, tarif3, price1, price2, price3, price1uzs, price2uzs, price3uzs = db.get_adv_prices()
	
	choosed_tarif = ''

	if tarif_num == '1':
		await state.update_data({'price': price1uzs})
		choosed_tarif = tarif1
		choosed_price = price1
		price_uzs = price1uzs
	elif tarif_num == '2':
		await state.update_data({'price': price2uzs})
		choosed_tarif = tarif2
		choosed_price = price2
		price_uzs = price2uzs
	elif tarif_num == '3':
		await state.update_data({'price': price3uzs})		
		choosed_tarif = tarif3
		choosed_price = price3
		price_uzs = price3uzs

	QIWI_TOKEN =  db.get_one('qiwi_wallet')
	p2p = QiwiP2P(auth_key=QIWI_TOKEN)
	comment = str(call.from_user.id) + '_' + call.from_user.full_name + '_' + str(randint(1, 9999))

	bill = p2p.bill(amount=int(choosed_price), lifetime=10, comment=comment)

	text = f"Siz <b>{choosed_tarif}</b> tarifni tanladingiz. Tarif narxi: {price_uzs} so'm ({choosed_price} RUB). To'lovni amalga oshirganingizdan so'ng reklamani yuborishingiz mumkin."
	await call.message.edit_text(text=text, reply_markup=check_pay(bill.pay_url, bill.bill_id, price_uzs, category='adv'))



@dp.message_handler(state=AdvSt.wait_for_screen, content_types='any')
async def screen_handler(msg: Message, state:FSMContext):
	await msg.answer("✅ Chek adming yuborildi. Endi reklamangizni yuboring...", reply_markup=cancel_btn)
	await AdvSt.wait_for_adv.set()

	for admin in ADMINS():
		try:
			await dp.bot.send_message(chat_id=admin, text = f"{msg.from_user.get_mention(as_html=True)} to'lov cheki yubordi👇", disable_web_page_preview=True)
			await asyncio.sleep(0.3)
			await msg.send_copy(chat_id=admin)
			await asyncio.sleep(0.3)
		except:
			pass


@dp.message_handler(state=AdvSt.wait_for_adv, content_types='any')
async def adv_handler(msg: Message, state:FSMContext):
	entities = msg.entities
	user_id = msg.from_user.id
	
	if db.get_one('avtopost') == 'aktiv':
		try:
			await dp.bot.send_copy(chat_id=-1001363526370)
			await msg.answer('✅ Kanalga joylandi', reply_markup=main_menu)
			db.add_ann('adver', avtopost=True)
		except:
			await msg.answer('Bot kanalga admin qilinmagan! Adminga murojaat qiling.')
			await dp.bot.send_message(chat_id=ADMINS()[0], text = "Bot kanalga admin qilinmagan!")

	else:
		await state.finish()
		await msg.answer("✅ Qabul qilindi! Reklamangiz admin tasdig'idan o'tgandan so'ng kanalga joylashiritiladi!",
			reply_markup=main_menu)
		ann_id = db.add_ann('adver')

		for admin in ADMINS():
			try:
				await dp.bot.send_message(chat_id=admin, text = f"{msg.from_user.get_mention(as_html=True)} reklama yubordi👇")
				await asyncio.sleep(0.3)
				await msg.send_copy(chat_id=admin, reply_markup=confirm_admin(user_id, ann_id))
				await asyncio.sleep(0.3)
			except:
				pass



@dp.callback_query_handler(text = 'cancel')
async def tarif_handler(call: CallbackQuery):
	await call.message.delete()
	await dp.send_message(chat_id=call.from_user.id, text="Asosiy menu", reply_markup=main_menu)