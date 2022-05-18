from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


admin_main = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton("📢 E'lon narxini sozlash⚙️")
		],
		[
			KeyboardButton("💸 Reklama narxini sozlash⚙️")
		],
		[
			KeyboardButton("💳 Hisob raqamlarni sozlash⚙️")
		],
		[
			KeyboardButton("🕹 Avtomatik yoki qo'lda rejimini sozlash⚙️")
		],
		[
			KeyboardButton("🕓 Vaqtni sozlash⚙️")
		]
	], resize_keyboard=True
)



adv_set_keyboard = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton("1-tarif ⚙️", callback_data='set-tarif-1'),
			InlineKeyboardButton("1-narx ⚙️", callback_data='set-price-1')
		],
		[
			InlineKeyboardButton("2-tarif ⚙️", callback_data='set-tarif-2'),
			InlineKeyboardButton("2-narx ⚙️", callback_data='set-price-2')
		],
		[
			InlineKeyboardButton("3-tarif ⚙️", callback_data='set-tarif-3'),
			InlineKeyboardButton("3-narx ⚙️", callback_data='set-price-3')
		],
	]
)


def set_avtopost_btn(status):
	markup = InlineKeyboardMarkup()

	if status == 'aktiv':
		markup.add(InlineKeyboardButton(text= "⛔️ O'chirish", callback_data='avtopost-aktiv emas'))
	elif status=='aktiv emas':
		markup.add(InlineKeyboardButton(text= "🔅 Yoqish", callback_data='avtopost-aktiv'))
	return markup


set_cards_keyboard = ReplyKeyboardMarkup(
	keyboard=[
		[
			InlineKeyboardButton(text="💳 KARTA RAQAMni o'zgartirish")
		],
		[
			InlineKeyboardButton(text="🍋 QIWI TOKENni o'zgartirish")
		],
		[
			InlineKeyboardButton(text="✖️ Bekor qilish")
		]
	], resize_keyboard=True
)