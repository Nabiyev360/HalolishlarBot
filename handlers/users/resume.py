from pyqiwip2p import QiwiP2P
from random import randint
from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncio import sleep

from loader import dp, db
from data.admins_list import ADMINS
from keyboards.inline.advKeyboards import check_pay
from keyboards.default.buttons import cancel_btn, confrim_btn
from keyboards.default.mainMenu import main_menu
from keyboards.inline.confirmAdmin import confirm_admin
from states.resumeStates import ResSt


@dp.message_handler(text = '📄 Rezyume joylashtirish')
async def resume_handler(message: types.Message, state: FSMContext):
    res = db.check_interval(message.from_user.id)
    if res == True:
        ann_price = db.get_one('ann_price')
        ann_price_uzs = db.get_one('ann_price_uzs')
        if ann_price != '0':
            txt = f"@Halolishlar kanaliga e'lon joylashtirish narxi {ann_price_uzs} so'm ({ann_price} RUB). To'lovni amalga oshirganingizdan so'ng rezyume joylashingiz mumkin."
            QIWI_TOKEN =  db.get_one('qiwi_wallet')
            p2p = QiwiP2P(auth_key=QIWI_TOKEN)
            comment = str(message.from_user.id) + '_' + message.from_user.full_name + '_' + str(randint(1, 9999))
            bill = p2p.bill(amount=int(ann_price), lifetime=10, comment=comment)        
            await message.answer(text=txt, reply_markup=check_pay(bill.pay_url, bill.bill_id, ann_price_uzs, category='res'))
        else:
            await message.answer(
                text = "1. Familiya, ism va sharfingizni kiriting.", 
                reply_markup=cancel_btn)
            await ResSt.input_name.set()
    else:
        interval, left_days = res
        await message.answer(f"Kanalga e'lon joylashtirish vaqti oralig'i {interval} kun. \nSiz {left_days} kundan so'ng yana e'lon joylashtirishingiz mumkin 💁‍♂️")


@dp.message_handler(state=ResSt.input_chek, content_types='any')
async def screen_handler(msg: types.Message, state:FSMContext):
    await msg.answer("✅ Chek adming yuborildi.", reply_markup=cancel_btn)
    await msg.answer(text = "1. Familiya, ism va sharfingizni kiriting.")
    await ResSt.input_name.set()

    for admin in ADMINS():
        try:
            await dp.bot.send_message(chat_id=admin, text = f"{msg.from_user.get_mention(as_html=True)} to'lov cheki yubordi👇", disable_web_page_preview=True)
            await sleep(0.3)
            await msg.send_copy(chat_id=admin)
            await sleep(0.3)
        except Exception as err:
            print(err)


@dp.message_handler(state=ResSt.input_name)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'name':message.text})
    await message.answer(
        text = "2. Tug'ilgan yil va sanangizni kiriting.",
        reply_markup=cancel_btn)
    await ResSt.input_birth.set()


@dp.message_handler(state=ResSt.input_birth)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'birth':message.text})

    await message.answer(
        text = "3. Yashash joyingizni kiriting (viloyat, shahar).", reply_markup=cancel_btn)
    await ResSt.input_region.set()


@dp.message_handler(state=ResSt.input_region)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'region':message.text})
    
    await message.answer(
        text = "4. Kasbingizni kiriting.\n\n\
Qanchalik aniq bo'lsa, shuncha yaxshi, masalan: \"Buxgalter\", \"Sotuv menejeri\".", reply_markup=cancel_btn)
    await ResSt.input_position.set()


@dp.message_handler(state=ResSt.input_position)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'position':message.text})
    
    await message.answer(
        text = "5. Bog'lanish uchun kontakt ma'lumotlaringizni kiriting.", reply_markup=cancel_btn)
    await ResSt.input_contact.set()


@dp.message_handler(state=ResSt.input_contact)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'contact':message.text})
    
    await message.answer(
        text = "6. Qancha ish haqi xohlaysiz?\n\n\
Qabul qilmoqchi bo'lgan miqdorni, shuningdek valyutani (USD / UZS) yozing.", reply_markup=cancel_btn)

    await ResSt.input_salary.set()


@dp.message_handler(state=ResSt.input_salary)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'salary':message.text})

    await message.answer(
        text = "7. Ish tajribangizni tavsiflab bering.\n\n\
Ish tajribangizni qisqacha va to'g'ri tasvirlab bering.\n\
Avval ishlagan joylaringizda sizning vazifangiz qanday bo'lganligi va qanday muvaffaqiyatlarga erishganingizni qisqacha tasvirlab berish juda muhimdir. \
Murakkab jumlalardan foydalanish shart emas. Hech bo'lmaganda, o'z so'zlaringiz bilan, nima qilolasiz, nima qildingiz, oldingi ish joyingizda nimani amalga oshirganingizni tasvirlab bering. Yutuqlaringiz haqida unutmang!", 
    reply_markup=cancel_btn)
    await ResSt.input_experience.set()


@dp.message_handler(state=ResSt.input_experience)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'experience':message.text})
    
    await message.answer(
        text = "8. O'qigan joylaringiz haqida gapirib bering.\n\n\
Boshlang'ich ta'lim teskari xronologik tartibda yoki muhimlik tartibida keltirilgan. Qo'shimcha ta'lim, agar u sizning yangi ishingizga a'loqasi bo'lsa uni tavsiflang.\n\
Misol:\n\
Toshkent davlat iqtisodiyot universiteti (2015-2019)", reply_markup=cancel_btn)

    await ResSt.input_education.set()


@dp.message_handler(state=ResSt.input_education)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'edu':message.text})
    
    await message.answer(
        text = "9. Kasbiy ko'nikmalarni ko'rsating.\n\n\
Misol:\n\
Savdo tajribasi (chakana savdoda 5 yil),\n\
Xodimlarni boshqarish qobiliyatlari (15 kishigacha bo'lgan jamoalar).", reply_markup=cancel_btn)

    await ResSt.input_skills.set()



@dp.message_handler(state=ResSt.input_skills)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'skills':message.text})
    
    await message.answer(
        text = "10. Tavsiyalarni qo'shing.\n\n\
Agar siz o'zingiz va ishingiz haqida ma'lumot bersangiz, \
sobiq rahbar yoki murabbiyning sizning sohangizda chinakam \
professional ekanligingiz haqidagi guvohligi dalil bo'lishi kerak.", reply_markup=cancel_btn)

    await ResSt.input_recommend.set()


@dp.message_handler(state=ResSt.input_recommend)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'recommend':message.text})
    
    await message.answer(
        text = "11. Qo'shimcha ma'lumotlarni kiriting.\n\n\
Bu yerda siz o'zingiz haqingizda ish beruvchining nazarida muhim bo'lishi mumkin bo'lgan qo'shimcha ma'lumotlarni taqdim etishingiz mumkin. Bundan avval kiritgan ko'nikmalaringizni takrorlamang!\n\
Misol:\n\
Energiya va xushmuomalalik menga samarali mahsulot taqdimotlarini o'tkazishga yordam beradi;\n\
Men tirishqoq va ehtiyotkorman, shuning uchun men yuqori mahsuldorlikni saqlab qolaman.", reply_markup=cancel_btn)

    await ResSt.input_additional.set()



@dp.message_handler(state=ResSt.input_additional)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'additional':message.text})
    
    await message.answer(
        text = "12. Portfolio'ingiz havolasini yuboring.\n\n\
Barcha qilgan ishlarimgizni bir joyda to'plang va unga havola yuboring.", reply_markup=cancel_btn)

    await ResSt.input_portfolio.set()


@dp.message_handler(state=ResSt.input_portfolio)
async def resume_handler(message: types.Message, state:FSMContext):
    await state.update_data({'portfolio':message.text})
    
    data = await state.get_data()
    text = f"#rezyume\n\n\
<b>👨‍💻 F. I. SH:</b> {data['name']}\n\
<b>🗓 Tug'ilgan yili:</b> {data['birth']}\n\
<b>📌 Yashash joyi:</b> {data['region']}\n\
<b>📄 Kasbi:</b> {data['position']}\n\
<b>📩 Aloqa:</b> {data['contact']}\n\
<b>💰 Ish haqi:</b> {data['salary']}\n\
<b>📈 Tajribasi:</b> {data['experience']}\n\
<b>🎓 O'qigan joylari:</b> {data['edu']}\n\
<b>📊 Kasbiy ko'nikmalari:</b> {data['skills']}\n\
<b>📋 Tavsiyalar:</b> {data['recommend']}\n\
<b>‼️ Qo'shimcha ma'lumot:</b> {data['additional']}\n\
<b>💼 Portfolio:</b> {data['portfolio']}\n\n\
👉🏻 Kanalga obuna bo'lish\n\
👨‍💻 @Halolishlar<a href='https://telegra.ph/file/7b99a6b7861774517d222.jpg'> </a>"
    await message.answer(text = text, reply_markup=cancel_btn)

    await message.answer("Barcha ma'lumotlar to'g'ri kiritilgan bo'lsa \"✅ Tasdiqlash\" tugmasini bosing.",
        reply_markup=confrim_btn)

    await ResSt.confirm_cancel.set()



@dp.message_handler(state=ResSt.confirm_cancel)
async def resume_handler(message: types.Message, state:FSMContext):
    data = await state.get_data()
    entities = message.entities
    user_id = message.from_user.id

    if message.text=='✅ Tasdiqlash':
        text = f"#rezyume\n\n\
<b>👨‍💻 F. I. SH.:</b> {data['name']}\n\
<b>🗓 Tug'ilgan yili:</b> {data['birth']}\n\
<b>📌 Yashash joyi:</b> {data['region']}\n\
<b>📄 Kasbi:</b> {data['position']}\n\
<b>📩 Aloqa:</b> {data['contact']}\n\
<b>💰 Ish haqi:</b> {data['salary']}\n\
<b>📈 Tajribasi:</b> {data['experience']}\n\
<b>🎓 O'qigan joylari:</b> {data['edu']}\n\
<b>📊 Kasbiy ko'nikmalari:</b> {data['skills']}\n\
<b>📋 Tavsiyalar:</b> {data['recommend']}\n\
<b>‼️ Qo'shimcha ma'lumot:</b> {data['additional']}\n\
<b>💼 Portfolio:</b> {data['portfolio']}\n\n\
👉🏻 Kanalga obuna bo'lish\n\
👨‍💻 @Halolishlar<a href='https://telegra.ph/file/7b99a6b7861774517d222.jpg'> </a>"

        if db.get_one('avtopost') == 'aktiv':
            try:
                await dp.bot.send_message(chat_id=-1001363526370, text= text, entities=entities, parse_mode='HTML')
                await message.answer('✅ Kanalga joylandi', reply_markup=main_menu)
                db.add_ann('resume', avtopost=True)
            except:
                await message.answer('Bot kanalga admin qilinmagan! Adminga murojaat qiling.', reply_markup=main_menu)
                await dp.bot.send_message(chat_id=ADMINS()[0], text = "Bot kanalga admin qilinmagan!")
        else:
            ann_id = db.add_ann('resume')
            await state.finish()
            for admin in ADMINS():
                try:
                    await dp.bot.send_message(chat_id=admin, text = f"#rezyume\n\n<b>👨‍💻 F. I. SH.:</b> {data['name']}\n<b>🗓 Tug'ilgan yili:</b> {data['birth']}\n<b>📌 Yashash joyi:</b> {data['region']}\n<b>📄 Kasbi:</b> {data['position']}\n<b>📩 Aloqa:</b> {data['contact']}\n<b>💰 Ish haqi:</b> {data['salary']}\n<b>📈 Tajribasi:</b> {data['experience']}\n<b>🎓 O'qigan joylari:</b> {data['edu']}\n<b>📊 Kasbiy ko'nikmalari:</b> {data['skills']}\n<b>📋 Tavsiyalar:</b> {data['recommend']}\n<b>‼️ Qo'shimcha ma'lumot:</b> {data['additional']}\n<b>💼 Portfolio:</b> {data['portfolio']}\n\n👉🏻 Kanalga obuna bo'lish\n👨‍💻 @Halolishlar<a href='https://telegra.ph/file/7b99a6b7861774517d222.jpg'> </a>", reply_markup=confirm_admin(user_id, ann_id))
                    await sleep(0.3)
                except Exception as err:
                    print(err)
            await message.answer(text = f"✅ Qabul qilindi! E'loningiz admin tasdig'idan o'tgandan so'ng @Halolishlar kanalida chop etiladi.", reply_markup=main_menu)        

    elif message.text=='❌ Bekor qilish':
        await message.answer("❌ Bekor qilindi. Siz asosiy menyudasiz.", reply_markup=main_menu)
        await state.finish()        
    else:
        await message.answer("Sizda yakunlanmagan e'lon joylashtirish holati mavjud. \
Yakunlash uchun quyidagilardan birini tanlang!", reply_markup=confrim_btn)