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
from keyboards.inline.advKeyboards import check_pay
from states.vacancyStates import VacSt


@dp.message_handler(text = '📢 Vakansiya joylashtirish')
async def vacancy_handler(message: types.Message, state: FSMContext):
    res = db.check_interval(message.from_user.id)
    if res == True:
        ann_price = db.get_one('ann_price')
        ann_price_uzs = db.get_one('ann_price_uzs')
        if ann_price != '0':
            txt = f"@Halolishlar kanaliga e'lon joylashtirish narxi {ann_price_uzs} so'm ({ann_price} RUB). To'lovni amalga oshirganingizdan so'ng vakansiya joylashingiz mumkin."
            QIWI_TOKEN =  db.get_one('qiwi_wallet')
            p2p = QiwiP2P(auth_key=QIWI_TOKEN)
            comment = str(message.from_user.id) + '_' + message.from_user.full_name + '_' + str(randint(1, 9999))
            bill = p2p.bill(amount=int(ann_price), lifetime=10, comment=comment)        
            await message.answer(text=txt, reply_markup=check_pay(bill.pay_url, bill.bill_id, ann_price_uzs, category='vac'))
        else:
            await message.answer(
                text = "1. Lavozim nomini kiriting.\n\nMisol: Kopirayter, Dasturchi, Dizayner, Savdo menejeri.", 
                reply_markup=cancel_btn)

            await VacSt.input_position.set()
    else:
        interval, left_days = res
        await message.answer(f"Kanalga e'lon joylashtirish vaqti oralig'i {interval} kun. \nSiz {left_days} kundan so'ng yana e'lon joylashtirishingiz mumkin 💁‍♂️")


@dp.message_handler(state=VacSt.input_chek, content_types='any')
async def screen_handler(msg: types.Message, state:FSMContext):
    await msg.answer("✅ Chek adming yuborildi.", reply_markup=cancel_btn)
    await msg.answer("1. Lavozim nomini kiriting.\n\nMisol: Kopirayter, Dasturchi, Dizayner, Savdo menejeri.")
    await VacSt.input_position.set()

    for admin in ADMINS():
        try:
            await dp.bot.send_message(chat_id=admin, text = f"{msg.from_user.get_mention(as_html=True)} to'lov cheki yubordi👇", disable_web_page_preview=True)
            await asyncio.sleep(0.3)
            await msg.send_copy(chat_id=admin)
            await asyncio.sleep(0.3)
        except:
            pass


@dp.message_handler(state=VacSt.input_position)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'position':message.text})

    await message.answer(
        text = "2. 🏢 Kompaniyangiz nomini kiriting.\n\nMisol: Facebook, Apple, Yandex.",
        reply_markup=cancel_btn)
    await VacSt.input_company.set()


@dp.message_handler(state=VacSt.input_company)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'company':message.text})
    
    await message.answer(
        text = "3. 👨‍💻 Xodim qanday vazifalarni bajarishi kerak?\n\nMisol:\n\
 ⁃ Videolarni montaj qilish\n\
 ⁃ Ma'lumotlar bazasini boshqarish\n\
 ⁃ Effetkli reklamalarni ishlab chiqish", reply_markup=cancel_btn)
    
    await VacSt.input_duties.set()



@dp.message_handler(state=VacSt.input_duties)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'duties':message.text})
    
    await message.answer(
        text = "4. ☝️ Nomzodga qo'yiladigan eng muhim talablarni ko'rsating.n\n\
Misol:\n\
 ⁃ WordPress bilan ishlash tajribasi;\n\
 ⁃ PHP bo'yicha yaxshi bilim;\n\
 ⁃ Yangi, yirik raqamli loyihalarda rivojlanish istagi;\n\
 ⁃ Jamoada ishlash ko'nikmalari;\n\
Ro'yxat qisqa va mazmunli bo'lishi kerak.\n\
Vaqtinchalik, mehnatsevarlik, ishni o‘z vaqtida yetkazib berish kabi fazilatlarni yozish shart emas.", 
        reply_markup=cancel_btn)
    await VacSt.input_important.set()



@dp.message_handler(state=VacSt.input_important)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'important':message.text})
    
    await message.answer(
        text = "5. ✅ Nomzodga qanday imtiyozlar va'da qilasiz?\n\n\
Misol:\n- do'stona jamoa;\n- individual ish jadvali\n5/2 soat 12:00 dan 18:00 gacha", reply_markup=cancel_btn)
    await VacSt.input_conditions.set()


@dp.message_handler(state=VacSt.input_conditions)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'conditions':message.text})
    
    await message.answer(
        text = "6. 💰 Ish haqini belgilang.\n\n\
Misol:\n - Oyiga 5 000 000 so'm\n - 600-1200 $  / oy\n - Suhbat natijasida.", reply_markup=cancel_btn)
    await VacSt.input_salary.set()


@dp.message_handler(state=VacSt.input_salary)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'salary':message.text})

    await message.answer(
        text = "7. 📩 Siz bilan qanday bog'lansam bo'ladi?\n\n\
Misol:\nDmitriy Alekseev +796966996 (ism va telefon raqami);\npochta@email.domen (pochta);\n@username (Telegramdagi foydalanuvchi nomi).", reply_markup=cancel_btn)
    await VacSt.input_contact.set()


@dp.message_handler(state=VacSt.input_contact)
async def vacancy_handler(message: types.Message, state:FSMContext):
    await state.update_data({'contact':message.text})
    
    data = await state.get_data()
    await message.answer(
        text = f"#vakansiya\n\
<b>{data['position']} kerak</b>\n\n\
<b>🏢 Kompaniya: </b>{data['company']}\n\
<b>👨‍💻 Ko'nikmalar:</b>\n{data['duties']}\n\
<b>☝️ Talablar:</b>\n{data['important']}\n\
<b>✅ Imtiyozlar:</b>\n{data['conditions']}\n\
<b>💰 Ish haqi:</b>\n{data['salary']}\n\
<b>📩 Aloqa:</b>\n{data['contact']}\n\n\
👉🏻 Kanalga obuna bo'lish\n\
👨‍💻 @Halolishlar<a href='https://telegra.ph/file/a8d4c1ae3debf7343b932.jpg'> </a>",
reply_markup=cancel_btn)

    await message.answer("Barcha ma'lumotlar to'g'ri kiritilgan bo'lsa \"✅ Tasdiqlash\" tugmasini bosing.",
        reply_markup=confrim_btn)

    await VacSt.confirm_cancel.set()



@dp.message_handler(state=VacSt.confirm_cancel)
async def vacancy_handler(message: types.Message, state:FSMContext):
    data = await state.get_data()
    entities = message.entities
    user_id = message.from_user.id
    
    if message.text=='✅ Tasdiqlash':
        await state.finish()
        if db.get_one('avtopost') == 'aktiv':
            try:
                await dp.bot.send_message(chat_id=-1001363526370, text= text, entities=entities, parse_mode='HTML')
                await message.answer('✅ Kanalga joylandi', reply_markup=main_menu)
                db.add_ann('vacancy', avtopost=True)

            except:
                await message.answer('Bot kanalga admin qilinmagan! Adminga murojaat qiling.', reply_markup=main_menu)
                await dp.bot.send_message(chat_id=ADMINS()[0], text = "Bot kanalga admin qilinmagan!")
        else:
            await message.answer(text = f"✅ Qabul qilindi! E'loningiz admin tasdig'idan o'tgandan so'ng @Halolishlar kanalida chop etiladi.", reply_markup=main_menu)
            await asyncio.sleep(0.3)
            for admin in ADMINS():
                try:
                    ann_id = db.add_ann('vacancy')
                    await dp.bot.send_message(chat_id=admin, text = f"#vakansiya\n<b>{data['position']} kerak</b>\n\n<b>🏢 Kompaniya: </b>{data['company']}\n<b>👨‍💻 Ko'nikmalar:</b>\n{data['duties']}\n<b>☝️ Talablar:</b>\n{data['important']}\n<b>✅ Imtiyozlar:</b>\n{data['conditions']}\n<b>💰 Ish haqi:</b>\n{data['salary']}\n<b>📩 Aloqa:</b>\n{data['contact']}\n\n👉🏻 Kanalga obuna bo'lish\n👨‍💻 @Halolishlar<a href='https://telegra.ph/file/a8d4c1ae3debf7343b932.jpg'> </a>", reply_markup=confirm_admin(user_id, ann_id))
                    await asyncio.sleep(0.3)
                except Exception as err:
                    print(err)

    elif message.text=='❌ Bekor qilish':
        await message.answer("❌ Bekor qilindi. Siz asosiy menyudasiz.", reply_markup=main_menu)
        await state.finish()

    else:
        await message.answer("Sizda yakunlanmagan e'lon joylashtirish holati mavjud. \
Yakunlash uchun quyidagilardan birini tanlang!", reply_markup=confrim_btn)