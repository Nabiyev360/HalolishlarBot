from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_btn = ReplyKeyboardMarkup(resize_keyboard=True,
	keyboard = [
		[
			KeyboardButton('❌ Bekor qilish')
		]
	]
)

admin_cancel_btn = ReplyKeyboardMarkup(resize_keyboard=True,
	keyboard = [
		[
			KeyboardButton('✖️ Bekor qilish')
		]
	]
)

confrim_btn = ReplyKeyboardMarkup(resize_keyboard=True,
	keyboard = [
		[
			KeyboardButton('✅ Tasdiqlash')
		],
		[
			KeyboardButton('❌ Bekor qilish')
		]
	]
)