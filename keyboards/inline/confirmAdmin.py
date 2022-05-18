from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


confirm_admin = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text='✅ Kanalga joylash', callback_data = 'admin-succes')
		],
		[
			InlineKeyboardButton(text='❌ Bekor qilish', callback_data = 'admin-cancel')
		]
	]
)