from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_admin(user_id, ann_id):
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='✅ Kanalga joylash', callback_data = 'admin-succes-"user_id":"{}", "ann_id":"{}"'.format(user_id, ann_id))
			],
			[
				InlineKeyboardButton(text='❌ Rad qilish', callback_data = 'admin-cancel-"user_id":"{}", "ann_id":"{}"'.format(user_id, ann_id))
			]
		]
	)

	return keyboard