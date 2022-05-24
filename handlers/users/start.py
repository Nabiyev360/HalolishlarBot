from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default.mainMenu import main_menu


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    user = msg.from_user
    db.add_user(user.id, user.full_name, user.username)
    await msg.answer(f"Salom {user.full_name}! O'zingizga kerakli bo'limni tanglang!", reply_markup=main_menu)