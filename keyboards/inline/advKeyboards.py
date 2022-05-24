from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def price_buttons(tarif1, tarif2, tarif3, price1, price2, price3):
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text=f"{tarif1}", callback_data='adv-tarif1'),
				InlineKeyboardButton(text=f"{tarif2}", callback_data='adv-tarif2')
			],
			[
				InlineKeyboardButton(text=f"{tarif3}", callback_data='adv-tarif3')
			]
		]
	)
	return keyboard

def check_pay(pay_url, bill_id, summa, category):
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text="To'lov qilish (UZCARD, HUMO)", callback_data=f'uzcard-humo-{summa}')
			],
			[
				InlineKeyboardButton(text="To'lov qilish (Visa, Qiwi)", url = pay_url)
			],
			[
				InlineKeyboardButton(text="To'lovni tekshirish", callback_data = f'{category}_check-{bill_id}')
			]
		]
	)
	return keyboard