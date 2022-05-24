import logging

from aiogram import Dispatcher


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(1589351394, "Bot ishga tushdi")

    except Exception as err:
        logging.exception(err)