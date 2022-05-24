from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


select_time = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text='🔹 Kunlik 📊', callback_data = 'select-day')
		],
		[
			InlineKeyboardButton(text='🔸 Oylik 📊', callback_data = 'select-month')
		],
		[
			InlineKeyboardButton(text='♦️ Yillik 📊', callback_data = 'select-year')
		],
		[
			InlineKeyboardButton(text='▫️Umumiy 📊', callback_data = 'select-all')
		]
	], 
)