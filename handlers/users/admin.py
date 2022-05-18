from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.config import ADMINS
from keyboards.default.adminKeyboards import admin_main, adv_set_keyboard, set_avtopost_btn, set_cards_keyboard
from keyboards.default.buttons import admin_cancel_btn
from states.settingStates import SetSt



@dp.message_handler(chat_id=ADMINS, commands=['admin'])
async def go_admin_panel(msg: Message):
	await msg.answer("Salom Admin! Siz admin paneldasiz.", reply_markup=admin_main)


@dp.callback_query_handler(chat_id=ADMINS, text_contains='admin-')
async def confirm_handler(call: CallbackQuery):
	image = "<a href='https://telegra.ph/file/5eaf44aa6b36eb6f3a45f.jpg'>  </a>"
	if call.message.text[:8] == '#rezyume':
		image = "<a href='https://telegra.ph/file/7b99a6b7861774517d222.jpg'> </a>"

	if call.data=='admin-succes':
		text = call.message.text
		entities = call.message.entities
		try:
			await dp.bot.send_message(chat_id=-1001363526370, text= text, entities=entities)
			await call.message.edit_text(text=call.message.text+f"\n\n<b>✅ Kanalga joylandi</b>{image}")
		except:
			await call.answer('Bot halol ishlar kanaliga admin qilinmagan!', show_alert=True)
		
		await dp.bot.send_message(chat_id=ADMINS[1], text= text, entities=entities)
	
	elif call.data=='admin-cancel':
		await call.message.edit_text(text=call.message.text+f"\n\n<b>❌ Bekor qilindi</b>{image}")



@dp.message_handler(chat_id=ADMINS, text="📢 E'lon narxini sozlash⚙️")
async def set_handler(msg: Message):
	text = f"E'lon berishning avvalgi narxi: <b>{db.get_one('ann_price')} RUB</b>.\nYangi narxni yuboring...\n\nNamuna: 100, 450 ..."
	await msg.answer(text=text, reply_markup=admin_cancel_btn)
	await SetSt.wait_ann_price.set()


@dp.message_handler(chat_id=ADMINS, state=SetSt.wait_ann_price)
async def set_handler(msg: Message, state:FSMContext):
	try:
		int(msg.text)
		db.update_value('ann_price', msg.text)
		await msg.answer(f"E'lon berish narxi yangilandi✅\nYangi narx: <b>{msg.text} RUB.</b>", reply_markup=admin_main)
		await state.finish()
	except:
		await msg.answer("Butun son yuboring")



@dp.message_handler(chat_id=ADMINS, text="💸 Reklama narxini sozlash⚙️")
async def set_handler(msg: Message):
	tarif1, tarif2, tarif3, price1, price2, price3 = db.get_adv_prices()
	text = f"Reklama berishning avvalgi narxlari:👇"
	text +=f"\n\n{tarif1} - {price1} rub.\n{tarif2} - {price2} rub.\n{tarif3} - {price3} rub."

	await msg.answer(text=text, reply_markup=adv_set_keyboard)



@dp.callback_query_handler(chat_id=ADMINS, text_contains='set-')
async def set_handler(call: CallbackQuery, state:FSMContext):
	num = call.data[-1]
	text = ''
	if 'tarif' in call.data:
		text = f"{num}-tarif haqida yangi ma'lumotni kiriting...\nNamuna: 2/24 soat, 4/doimiy, ..."
		param = 'tarif' + num

	elif 'price' in call.data:
		text = f"{num}-tarifning yangi narxini kiriting...\nNamuna: 100, 500, ..."
		param = 'price' + num

	await call.message.answer(text=text, reply_markup=admin_cancel_btn)
	await call.message.delete()

	await SetSt.wait_adv_value.set()
	await state.update_data({'set-param':param})



@dp.message_handler(chat_id=ADMINS, state=SetSt.wait_adv_value)
async def set_handler(msg: Message, state:FSMContext):
	data = await state.get_data()
	param = data['set-param']
	num = param[-1]

	if 'tarif' in param:
		db.update_value(param, msg.text)
		await msg.answer(f"{num}-Ta'rif ma'lumoti yangilandi✅\nYangi ma'lumot: <b>{msg.text}</b>", reply_markup=admin_main)
		await state.finish()
	
	elif 'price' in param:
		try:
			int(msg.text)
			db.update_value(param, msg.text)
			await msg.answer(f"{num}-Ta'rif narxi yangilandi✅\nYangi narx: <b>{msg.text} RUB.</b>", reply_markup=admin_main)
			await state.finish()
		except:
			await msg.answer("Butun son yuboring")



@dp.message_handler(chat_id=ADMINS, text='💳 Hisob raqamlarni sozlash⚙️')
async def set_handler(msg: Message):
	await msg.answer("Qaysi hisob raqamni o'zgartirmoqchisiz?", reply_markup=set_cards_keyboard)



@dp.message_handler(chat_id=ADMINS, text="💳 KARTA RAQAMni o'zgartirish")
async def set_handler(msg: Message):
	uzcard_num = db.get_one('uzcard_num')
	await msg.answer(f"Ayni paytdagi karta raqam: {uzcard_num}\n\n O'zgartirish uchun yangi karta raqamni yuboring.", reply_markup=admin_cancel_btn)
	await SetSt.wait_uzcard_num.set()


@dp.message_handler(chat_id=ADMINS, state=SetSt.wait_uzcard_num)
async def set_handler(msg: Message, state:FSMContext):
	try:
		int(msg.text)
		if len(msg.text) > 10:
			db.update_value('uzcard_num', msg.text)
			await msg.answer("Karta raqam yangilandi ✅", reply_markup=admin_main)
			await state.finish()
		else:
			1/0
	except:
		await msg.answer("Karta raqam nostandart. Qayta kiriting...", reply_markup=admin_cancel_btn)



@dp.message_handler(chat_id=ADMINS, text="🍋 QIWI TOKENni o'zgartirish")
async def set_handler(msg: Message):
	QIWI_TOKEN = db.get_one('qiwi_wallet')
	await msg.answer(f"Hozirgi QIWI TOKEN - <code>{QIWI_TOKEN}</code>\n\n O'zgartirish uchun yangi tokenni yuboring...", reply_markup=admin_cancel_btn)

	await SetSt.wait_qiwi_token.set()


@dp.message_handler(chat_id=ADMINS, state=SetSt.wait_qiwi_token)
async def set_handler(msg: Message, state:FSMContext):
	if len(msg.text) < 30:
		await msg.answer("Token nostandart. Qayta kiriting...", reply_markup=admin_cancel_btn)
	else:
		db.update_value('qiwi_wallet', msg.text)
		await msg.answer("Qiwi token yangilandi ✅", reply_markup=admin_main)

		await state.finish()


@dp.message_handler(chat_id=ADMINS, text = "🕹 Avtomatik yoki qo'lda rejimini sozlash⚙️")
async def set_handler(msg: Message, state:FSMContext):
	status = db.get_one('avtopost')
	await msg.answer(f"🕹 Avtomatik rejim {status}.", reply_markup=set_avtopost_btn(status))


@dp.callback_query_handler(chat_id=ADMINS, text_contains='avtopost-')
async def set_handler(call: CallbackQuery, state:FSMContext):
	new_status = call.data[9:]
	status = db.get_one('avtopost')
	db.update_value('avtopost', new_status)
	await call.message.edit_text(text=f"🕹 Avtomatik rejim {new_status}.", reply_markup=set_avtopost_btn(new_status))



@dp.message_handler(chat_id=ADMINS, text = "🕓 Vaqtni sozlash⚙️")
async def set_handler(msg: Message):
	interval = db.get_one('post_interval')
	await msg.answer(f"E'lon joylash interval muddati {interval} kun. O'zgartirish uchun yangi muddatni kiriting...\n\nNamuna: 1, 3, 7, ...", reply_markup=admin_cancel_btn)
	await SetSt.wait_interval.set()

@dp.message_handler(chat_id=ADMINS, state=SetSt.wait_interval)
async def set_handler(msg: CallbackQuery, state:FSMContext):
	try:
		int(msg.text)
		db.update_value('post_interval', msg.text)
		await msg.answer(f"E'lon joylash intervali yangilandi✅\nYangi interval: <b>{msg.text} kun.</b>", reply_markup=admin_main)
		await state.finish()
	except:
		await msg.answer("Butun son yuboring")