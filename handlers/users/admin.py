import json
import asyncio
from aiogram.types import Message, CallbackQuery, ForceReply, ContentType, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.admins_list import ADMINS
from keyboards.default.adminKeyboards import admin_main, adv_set_keyboard, set_avtopost_btn, set_cards_keyboard
from keyboards.default.buttons import admin_cancel_btn
from keyboards.inline.statsKeyboard import select_time
from states.settingStates import SetSt



@dp.message_handler(commands=['admin'])
async def go_admin_panel(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		await msg.answer("Salom Admin! Siz admin paneldasiz.", reply_markup=admin_main)


@dp.callback_query_handler(text_contains='admin-')
async def confirm_handler(call: CallbackQuery):
	button_data = json.loads("{"+call.data[13:]+"}")
	user_id = button_data['user_id']
	ann_id = button_data['ann_id']

	image = ""
	txt = call.message.text
	
	if txt == None:
		txt = call.message.caption
		if txt == None:
			txt = ''

	elif call.message.text[:8] == '#rezyume':
		image = "<a href='https://telegra.ph/file/7b99a6b7861774517d222.jpg'> </a>"
	elif call.message.text[:10] == '#xizmatlar':
		image = "<a href='https://telegra.ph/file/508a608f67396ac5b84ed.jpg'> </a>"
	elif call.message.text[:10] == '#vakansiya':
		image = "<a href='https://telegra.ph/file/a8d4c1ae3debf7343b932.jpg'> </a>"

	if 'admin-succes' in call.data:
		entities = call.message.entities
		try:
			if txt != '' and txt != None:
				await dp.bot.send_message(chat_id=-1001363526370, text= txt, entities=entities)
			else:
				await call.message.send_copy(1589351394, reply_markup=ReplyKeyboardRemove())
			
			if call.message.text != None:
				await call.message.edit_text(text=txt+f"\n\n<b>✅ Kanalga joylandi</b>{image}")
			else:
				await call.message.edit_caption(caption='✅ Kanalga joylandi')
				db.update_interval(int(user_id))
			db.check_ann(ann_id, True)
		except Exception as err:
			await call.answer('Bot halol ishlar kanaliga admin qilinmagan!', show_alert=True)
			print(err)

	elif 'admin-cancel' in call.data:
		if call.message.text != None:
			await call.message.edit_text(text=txt+f"\n\n<b>❌ Rad qilindi</b>{image}")
		else:
			await call.message.edit_caption(caption=txt+f"\n\n<b>❌ Rad qilindi</b>{image}")
		await call.message.answer(f"❕ Rad qilinish sababini yuboring (yuborish ixtiyoriy, istasangiz /bekor qiling.<a href='https://{user_id}.bb'> </a>", reply_markup=ForceReply(), disable_web_page_preview=True)
		db.check_ann(ann_id, False)



@dp.message_handler(text="📢 E'lon narxini sozlash⚙️ | RUB")
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		text = f"E'lon berishning avvalgi narxi: <b>{db.get_one('ann_price')} RUB</b>.\nYangi narxni yuboring...\n\nNamuna: 100, 450 ..."
		await msg.answer(text=text, reply_markup=admin_cancel_btn)
		await SetSt.wait_ann_price.set()


@dp.message_handler(state=SetSt.wait_ann_price)
async def set_handler(msg: Message, state:FSMContext):
	try:
		int(msg.text)
		db.update_value('ann_price', msg.text)
		await msg.answer(f"E'lon berish narxi yangilandi✅\nYangi narx: <b>{msg.text} RUB.</b>", reply_markup=admin_main)
		await state.finish()
	except:
		await msg.answer("Butun son yuboring")


@dp.message_handler(text="📢 E'lon narxini sozlash⚙️ | UZS")
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		text = f"E'lon berishning avvalgi narxi: <b>{db.get_one('ann_price_uzs')} UZS</b>.\nYangi narxni yuboring...\n\nNamuna: 60000, 110000, ..."
		await msg.answer(text=text, reply_markup=admin_cancel_btn)
		await SetSt.wait_ann_price_uzs.set()

@dp.message_handler(state=SetSt.wait_ann_price_uzs)
async def set_handler(msg: Message, state:FSMContext):
	try:
		int(msg.text)
		db.update_value('ann_price_uzs', msg.text)
		await msg.answer(f"E'lon berish narxi yangilandi✅\nYangi narx: <b>{msg.text} UZS.</b>", reply_markup=admin_main)
		await state.finish()
	except:
		await msg.answer("Butun son yuboring")



@dp.message_handler(text="💸 Reklama narxini sozlash⚙️")
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		tarif1, tarif2, tarif3, price1, price2, price3, price1uzs, price2uzs, price3uzs = db.get_adv_prices()
		text = f"Reklama berishning avvalgi narxlari:👇"
		text +=f"\n\n{tarif1} - {price1uzs} so'm | {price1} rub.\n{tarif2} - {price2uzs} so'm | {price2} rub.\n{tarif3} - {price3uzs} so'm | {price3} rub."

		await msg.answer(text=text, reply_markup=adv_set_keyboard)

@dp.callback_query_handler(text_contains='set-')
async def set_handler(call: CallbackQuery, state:FSMContext):
	num = call.data[-1]
	text = ''
	if 'uzs' in call.data:
		text = f"{num}-tarifning yangi narxini (UZS) kiriting...\nNamuna: 40000, 90000, ..."
		param = 'price' + num + 'uzs'

	elif 'tarif' in call.data:
		text = f"{num}-tarif haqida yangi ma'lumotni kiriting...\nNamuna: 2/24 soat, 4/doimiy, ..."
		param = 'tarif' + num

	elif 'price' in call.data:
		text = f"{num}-tarifning yangi narxini (RUB) kiriting...\nNamuna: 100, 500, ..."
		param = 'price' + num

	await call.message.answer(text=text, reply_markup=admin_cancel_btn)
	await call.message.delete()

	await SetSt.wait_adv_value.set()
	await state.update_data({'set-param':param})



@dp.message_handler(state=SetSt.wait_adv_value)
async def set_handler(msg: Message, state:FSMContext):
	data = await state.get_data()
	param = data['set-param']
	num = param[-1]
	if 'uzs' in param:
		num = param[5]

	if 'uzs' in param:
		try:
			int(msg.text)
			db.update_value(param, msg.text)
			await msg.answer(f"{num}-Ta'rif narxi (UZS) yangilandi✅\nYangi narx: <b>{msg.text} UZS.</b>", reply_markup=admin_main)
			await state.finish()
		except:
			await msg.answer("Butun son yuboring")


	elif 'tarif' in param:
		db.update_value(param, msg.text)
		await msg.answer(f"{num}-Ta'rif ma'lumoti yangilandi✅\nYangi ma'lumot: <b>{msg.text}</b>", reply_markup=admin_main)
		await state.finish()
	
	elif 'price' in param:
		try:
			int(msg.text)
			db.update_value(param, msg.text)
			await msg.answer(f"{num}-Ta'rif narxi (RUB) yangilandi✅\nYangi narx: <b>{msg.text} RUB.</b>", reply_markup=admin_main)
			await state.finish()
		except:
			await msg.answer("Butun son yuboring")



@dp.message_handler(text='💳 Hisob raqamlarni sozlash⚙️')
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		await msg.answer("Qaysi hisob raqamni o'zgartirmoqchisiz?", reply_markup=set_cards_keyboard)



@dp.message_handler(text="💳 KARTA RAQAMni o'zgartirish")
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		uzcard_num = db.get_one('uzcard_num')
		await msg.answer(f"Ayni paytdagi karta raqam: {uzcard_num}\n\n O'zgartirish uchun yangi karta raqamni yuboring.", reply_markup=admin_cancel_btn)
		await SetSt.wait_uzcard_num.set()


@dp.message_handler(state=SetSt.wait_uzcard_num)
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



@dp.message_handler(chat_id=ADMINS(), text="🍋 QIWI TOKENni o'zgartirish")
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		QIWI_TOKEN = db.get_one('qiwi_wallet')
		await msg.answer(f"Hozirgi QIWI TOKEN - <code>{QIWI_TOKEN}</code>\n\n O'zgartirish uchun yangi tokenni yuboring...", reply_markup=admin_cancel_btn)

		await SetSt.wait_qiwi_token.set()


@dp.message_handler(state=SetSt.wait_qiwi_token)
async def set_handler(msg: Message, state:FSMContext):
	if len(msg.text) < 30:
		await msg.answer("Token nostandart. Qayta kiriting...", reply_markup=admin_cancel_btn)
	else:
		db.update_value('qiwi_wallet', msg.text)
		await msg.answer("Qiwi token yangilandi ✅", reply_markup=admin_main)

		await state.finish()


@dp.message_handler(text = "🕹 Avtomatik yoki qo'lda rejimini sozlash⚙️")
async def set_handler(msg: Message, state:FSMContext):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		status = db.get_one('avtopost')
		await msg.answer(f"🕹 Avtomatik rejim {status}.", reply_markup=set_avtopost_btn(status))


@dp.callback_query_handler(text_contains='avtopost-')
async def set_handler(call: CallbackQuery, state:FSMContext):
		new_status = call.data[9:]
		status = db.get_one('avtopost')
		db.update_value('avtopost', new_status)
		await call.message.edit_text(text=f"🕹 Avtomatik rejim {new_status}.", reply_markup=set_avtopost_btn(new_status))



@dp.message_handler(text = "🕓 Vaqtni sozlash")
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		interval = db.get_one('post_interval')
		await msg.answer(f"E'lon joylash interval muddati {interval} kun. O'zgartirish uchun yangi muddatni kiriting...\n\nNamuna: 1, 3, 7, ...", reply_markup=admin_cancel_btn)
		await SetSt.wait_interval.set()

@dp.message_handler(state=SetSt.wait_interval)
async def set_handler(msg: CallbackQuery, state:FSMContext):
	try:
		int(msg.text)
		db.update_value('post_interval', msg.text)
		await msg.answer(f"E'lon joylash intervali yangilandi✅\nYangi interval: <b>{msg.text} kun.</b>", reply_markup=admin_main)
		await state.finish()
	except:
		await msg.answer("Butun son yuboring")



@dp.message_handler(text = '👨‍💼 Admin tayinlash')
async def set_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		text = "Adminlar ro'yxati:\n\n"

		names = db.get_admins('full_name')
		ids = db.get_admins()
		n = 0
		for name in names:
			text += f'👨‍💼 {name[0]} <code>{ids[n][0]}</code>\n'
			n+=1
		text += "\n👉 Admin qilib tayinlamoqchi bo'lgan foydalanuvchining Telegram ID'sini yuboring. (ID ni olish uchun @username_to_id_bot ga foydalanuvchi username'ini yuboring)"
		text += "\n\n👉 Adminni o'chirish uchun admin ID'sini yuboring (ID admin ismi yonida)."

		
		await msg.answer(text = text, reply_markup=admin_cancel_btn)
		await SetSt.wait_admin_id.set()


@dp.message_handler(state=SetSt.wait_admin_id)
async def set_handler(msg: Message, state: FSMContext):
	try:
		int(msg.text)
		res = db.add_admin(msg.text)
		await msg.answer(res, reply_markup=admin_main)
		await state.finish()
	except:
		await msg.answer('ID nostandart qayta kiriting...')


# Reklama yuborish
@dp.message_handler(text = '✉️ Xabar yuborish')
async def send_message_users(message: Message):
	user_id = message.from_user.id
	if user_id in ADMINS():
	    await message.answer(text = "Foydalanuvchilarga yuborish kerak bo'lgan xabarni yuboring🔼\n\nBekor qilish uchun \"Cancel\"ni bosing",
	        reply_markup = admin_cancel_btn)
	    await SetSt.waiting_admin_message.set()


@dp.message_handler(state = SetSt.waiting_admin_message, content_types= ContentType.ANY)
async def send_message_users(message:Message, state:FSMContext):
    await state.finish()
    await message.answer('Xabar foydalanuvchilarga yuborilmoqda...', reply_markup=admin_main)
    n = 0
    for i in db.get_users_id():
        user_id = i[0]
        try:
            await message.send_copy(chat_id = user_id)
            n+=1
        except:
            pass
        await asyncio.sleep(0.3)
    await message.answer(f'Xabar {n} ta foydalanuvchiga muvaffaqqiyatli yuborildi!')



@dp.message_handler(text = "📊 Statistika")
async def couse_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		total_anns, total_vac, total_ser, total_res, total_rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count = db.get_stats('all')

		txt = f'<b>📊 UMUMIY STATISTIKA\n\n👥 Barcha foydalanuvchilar:</b> {users_count} ta'
		txt += f"\n\n<b>📮 Barcha e'lonlar:</b> {total_anns} ta"
		txt += f"\n<b>✅ Kanalga joylangan:</b> {check_anns}"
		txt += f"\n\n<b>🟦 Barcha vakansiyalar:</b> {total_vac}"
		txt += f"\n<b>🔵 Joylangan vakansiyalar:</b> {check_vac}"
		txt += f"\n\n<b>🟨 Barcha xizmatlar:</b> {total_ser}"
		txt += f"\n<b>🟡 Joylangan xizmatlar:</b> {check_ser}"
		txt += f"\n\n<b>🟪 Barcha rezyumelar:</b> {total_res}"
		txt += f"\n<b>🟣 Joylangan rezyumelar:</b> {check_res}"
		txt += f"\n\n<b>🟩 Barcha reklamalar:</b> {total_rek}"
		txt += f"\n<b>🟢 Joylangan reklamalar:</b> {check_rek}"

		
		await msg.answer(txt, reply_markup=select_time)


@dp.callback_query_handler(text_contains = 'select-')
async def couse_handler(call: CallbackQuery):
	time = call.data[7:]
	data = db.get_stats(time)
	anns, vac, ser, res, rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count = data
	if time == 'day':
		txt = f'<b>📊 KUNLIK STATISTIKA\n\n👥 Qo\'shilgan foydalanuvchilar:</b> {users_count} ta'
	elif time == 'month':
		txt = f'<b>📊 OYLIK STATISTIKA\n\n👥 Qo\'shilgan foydalanuvchilar:</b> {users_count} ta'
	elif time == 'year':
		txt = f'<b>📊 YILLIK STATISTIKA\n\n👥 Qo\'shilgan foydalanuvchilar:</b> {users_count} ta'
	elif time == 'all':
		txt = f'<b>📊 UMUMIY STATISTIKA\n\n👥 Qo\'shilgan foydalanuvchilar:</b> {users_count} ta'
		anns, vac, ser, res, rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count = data



	txt += f"\n\n<b>📮 Kelgan e'lonlar:</b> {anns} ta"
	txt += f"\n<b>✅ Kanalgan joylangan:</b> {check_anns}"
	txt += f"\n\n<b>🟦 Kelgan vakansiyalar:</b> {vac}"
	txt += f"\n<b>🔵 Joylangan vakansiyalar:</b> {check_vac}"
	txt += f"\n\n<b>🟨 Kelgan xizmatlar:</b> {ser}"
	txt += f"\n<b>🟡 Joylangan xizmatlar:</b> {check_ser}"
	txt += f"\n\n<b>🟪 Kelgan rezyumelar:</b> {res}"
	txt += f"\n<b>🟣 Joylangan rezyumelar:</b> {check_res}"
	txt += f"\n\n<b>🟩 Kelgan reklamalar:</b> {rek}"
	txt += f"\n<b>🟢 Joylangan reklamalar:</b> {check_rek}"

	try:
		await call.message.edit_text(text = txt, reply_markup=select_time)
	except:
		pass





@dp.message_handler(is_reply=True)
async def couse_handler(msg: Message):
	user_id = msg.from_user.id
	if user_id in ADMINS():
		try:
			client_id = msg.reply_to_message.entities[1].url[8:-4]
			txt = f"❌ E'loningiz rad etildi!\n\nSabab: <b>{msg.text}</b>"
			await dp.bot.send_message(chat_id=client_id, text=txt)
			await msg.answer("Xabar yuborildi ✅", reply_markup=admin_main)
		except:
			pass

