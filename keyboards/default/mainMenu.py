from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(resize_keyboard=True,
	keyboard = [
		[
			KeyboardButton('📢 Vakansiya joylashtirish')
		],
		[
			KeyboardButton('🛠 Xizmatlar joylashtirish')
		],
		[
			KeyboardButton('📄 Rezyume joylashtirish')
		],
		[
			KeyboardButton('💸 Reklama joylashtirish')
		]
	]
)