import asyncio
from pyqiwip2p import QiwiP2P
from random import randint
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.admins_list import ADMINS
from keyboards.inline.advKeyboards import check_pay
from keyboards.default.buttons import cancel_btn, confrim_btn
from keyboards.default.mainMenu import main_menu
from keyboards.inline.confirmAdmin import confirm_admin
from states.serviceStates import SerSt


@dp.message_handler(text = '🛠 Xizmatlar joylashtirish')
async def service_handler(message: types.Message, state: FSMContext):
    res = db.check_interval(message.from_user.id)
    if res == True:
        ann_price = db.get_one('ann_price')
        ann_price_uzs = db.get_one('ann_price_uzs')
        if ann_price != '0':
            txt = f"@Halolishlar kanaliga e'lon joylashtirish narxi {ann_price_uzs} so'm ({ann_price} RUB). To'lovni amalga oshirganingizdan so'ng xizmatlaringizni joylashingiz mumkin."
            QIWI_TOKEN =  db.get_one('qiwi_wallet')
            p2p = QiwiP2P(auth_key=QIWI_TOKEN)
            comment = str(message.from_user.id) + '_' + message.from_user.full_name + '_' + str(randint(1, 9999))
            bill = p2p.bill(amount=int(ann_price), lifetime=10, comment=comment)
            await message.answer(text=txt, reply_markup=check_pay(bill.pay_url, bill.bill_id, ann_price_uzs, category='ser'))
        else:
            await message.answer(
                text = "1. Xizmat turini kiriting.\n\nMisol: Yuk tashish, Enagalik xizmati, Shaxsiy o'qituvchi", 
                reply_markup=cancel_btn)
            await SerSt.input_service_name.set()
    else:
        interval, left_days = res
        await message.answer(f"Kanalga e'lon joylashtirish vaqti oralig'i {interval} kun. \nSiz {left_days} kundan so'ng yana e'lon joylashtirishingiz mumkin 💁‍♂️")


@dp.message_handler(state=SerSt.input_chek, content_types='any')
async def screen_handler(msg: types.Message, state:FSMContext):
    await msg.answer("✅ Chek adming yuborildi.", reply_markup=cancel_btn)
    await msg.answer("1. Xizmat turini kiriting.\n\nMisol: Yuk tashish, Enagalik xizmati, Shaxsiy o'qituvchi")
    await SerSt.input_service_name.set()

    for admin in ADMINS():
        try:
            await dp.bot.send_message(chat_id=admin, text = f"{msg.from_user.get_mention(as_html=True)} to'lov cheki yubordi👇", disable_web_page_preview=True)
            await asyncio.sleep(0.3)
            await msg.send_copy(chat_id=admin)
            await asyncio.sleep(0.3)
        except:
            pass




@dp.message_handler(state=SerSt.input_service_name)
async def service_handler(message: types.Message, state:FSMContext):
    await state.update_data({'service_name':message.text})

    await message.answer(
        text = "2. Xizmat ko'rsatish manzilini kiriting (Viloyat, shahar)",
        reply_markup=cancel_btn)
    await SerSt.input_service_region.set()


@dp.message_handler(state=SerSt.input_service_region)
async def service_handler(message: types.Message, state:FSMContext):
    await state.update_data({'service_region':message.text})
    
    await message.answer(
        text = "3. Xizmat narxini kiriting", reply_markup=cancel_btn)
    
    await SerSt.input_service_price.set()



@dp.message_handler(state=SerSt.input_service_price)
async def service_handler(message: types.Message, state:FSMContext):
    await state.update_data({'service_price':message.text})
    
    await message.answer(
        text = "4. Bog'lanish uchun kontaktni kiriting.\n\n -Telefon raqam\n -Telegram username", 
        reply_markup=cancel_btn)
    await SerSt.input_service_contact.set()



@dp.message_handler(state=SerSt.input_service_contact)
async def service_handler(message: types.Message, state:FSMContext):
    await state.update_data({'service_contact':message.text})    
    data = await state.get_data()

    await message.answer(
        text = f"#xizmatlar\n\
<b>🛠 Xizmat turi:</b> {data['service_name']}\n\n\
<b>📍 Manzil:</b> {data['service_region']}\n\
<b>💰 Xizmat narxi:</b> {data['service_price']}\n\
<b>📩 Aloqa:</b> {data['service_contact']}\n\n\
👉🏻 Kanalga obuna bo'lish\n\
👨‍💻 @Halolishlar<a href='https://telegra.ph/file/508a608f67396ac5b84ed.jpg'> </a>",
reply_markup=cancel_btn)

    await message.answer("Barcha ma'lumotlar to'g'ri kiritilgan bo'lsa \"✅ Tasdiqlash\" tugmasini bosing.",
        reply_markup=confrim_btn)

    await SerSt.service_confirm_cancel.set()



@dp.message_handler(state=SerSt.service_confirm_cancel)
async def service_handler(message: types.Message, state:FSMContext):
    data = await state.get_data()
    entities = message.entities
    user_id = message.from_user.id
        
    text = f"#xizmatlar\n\
<b>🛠 Xizmat turi:</b> {data['service_name']}\n\n\
<b>📍 Manzil:</b> {data['service_region']}\n\
<b>💰 Xizmat narxi:</b> {data['service_price']}\n\
<b>📩 Aloqa:</b> {data['service_contact']}\n\n\
👉🏻 Kanalga obuna bo'lish\n\
👨‍💻 @Halolishlar<a href='https://telegra.ph/file/508a608f67396ac5b84ed.jpg'> </a>"

    if message.text=='✅ Tasdiqlash':
        if db.get_one('avtopost') == 'aktiv':
            try:
                await dp.bot.send_message(chat_id=-1001363526370, text= text, entities=entities, parse_mode='HTML')
                await message.answer('✅ Kanalga joylandi', reply_markup=main_menu)
                db.add_ann('service', avtopost=True)
            except Exception as err:
                print(err)
                await message.answer('Bot kanalga admin qilinmagan! Adminga murojaat qiling.', reply_markup=main_menu)
                await dp.bot.send_message(chat_id=ADMINS()[0], text = "Bot kanalga admin qilinmagan!")
        else:
            await state.finish()
            for admin in ADMINS():
                try:
                    ann_id = db.add_ann('service')
                    await dp.bot.send_message(chat_id=admin, text = text, reply_markup=confirm_admin(user_id, ann_id))
                    await asyncio.sleep(0.3)
                except Exception as ex:
                    print(ex)
            await message.answer(text = f"✅ Qabul qilindi! E'loningiz admin tasdig'idan o'tgandan so'ng @Halolishlar kanalida chop etiladi.", reply_markup=main_menu)

    elif message.text=='❌ Bekor qilish':
        await message.answer("❌ Bekor qilindi. Siz asosiy menyudasiz.", reply_markup=main_menu)
        await state.finish()

    else:
        await message.answer("Sizda yakunlanmagan elon joylashtirish holati mavjud. \
Yakunlash uchun quyidagilardan birini tanlang!", reply_markup=confrim_btn)