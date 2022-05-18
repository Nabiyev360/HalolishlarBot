from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncio import sleep

from loader import dp
from data.config import ADMINS
from keyboards.default.buttons import cancel_btn, confrim_btn
from keyboards.default.mainMenu import main_menu
from keyboards.inline.confirmAdmin import confirm_admin
from states.vacancyStates import VacSt


@dp.message_handler(text = '📢 Vakansiya joylashtirish')
async def vacancy_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text = "1. Lavozim nomini kiriting.\n\nMisol: Kopirayter, Dasturchi, Dizayner, Savdo menejeri.", 
        reply_markup=cancel_btn)

    await VacSt.input_position.set()


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
Misol:\nOyiga 50 000 rubl\n600-1200 $  / oy\nSuhbat natijasida.", reply_markup=cancel_btn)
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
👨‍💻 @Halolishlar<a href='https://telegra.ph/file/5eaf44aa6b36eb6f3a45f.jpg'> </a>",
reply_markup=cancel_btn)

    await message.answer("Barcha ma'lumotlar to'g'ri kiritilgan bo'lsa \"✅ Tasdiqlash\" tugmasini bosing.",
        reply_markup=confrim_btn)

    await VacSt.confirm_cancel.set()



@dp.message_handler(state=VacSt.confirm_cancel)
async def vacancy_handler(message: types.Message, state:FSMContext):
    data = await state.get_data()
    
    if message.text=='✅ Tasdiqlash':
        try: 
            await dp.bot.send_message(chat_id=ADMINS[0], 
                text = f"#vakansiya\n<b>{data['position']} kerak</b>\n\n<b>🏢 Kompaniya: </b>{data['company']}\n<b>👨‍💻 Ko'nikmalar:</b>\n{data['duties']}\n<b>☝️ Talablar:</b>\n{data['important']}\n<b>✅ Imtiyozlar:</b>\n{data['conditions']}\n<b>💰 Ish haqi:</b>\n{data['salary']}\n<b>📩 Aloqa:</b>\n{data['contact']}\n\n👉🏻 Kanalga obuna bo'lish\n👨‍💻 @Halolishlar<a href='https://telegra.ph/file/5eaf44aa6b36eb6f3a45f.jpg'> </a>",
                reply_markup=confirm_admin)
            await dp.bot.send_message(chat_id=ADMINS[1], 
                text = f"#vakansiya\n<b>{data['position']} kerak</b>\n\n<b>🏢 Kompaniya: </b>{data['company']}\n<b>👨‍💻 Ko'nikmalar:</b>\n{data['duties']}\n<b>☝️ Talablar:</b>\n{data['important']}\n<b>✅ Imtiyozlar:</b>\n{data['conditions']}\n<b>💰 Ish haqi:</b>\n{data['salary']}\n<b>📩 Aloqa:</b>\n{data['contact']}\n\n👉🏻 Kanalga obuna bo'lish\n👨‍💻 @Halolishlar<a href='https://telegra.ph/file/5eaf44aa6b36eb6f3a45f.jpg'> </a>",
                reply_markup=confirm_admin)
            await sleep(0.3)
            await message.answer(
                text = f"✅ Qabul qilindi! E'loningiz admin tasdig'idan o'tgandan so'ng @Halolishlar kanalida chop etiladi.",
                reply_markup=main_menu)
            await state.finish()
        except:
            pass
    elif message.text=='❌ Bekor qilish':
        await message.answer("❌ Bekor qilindi. Siz asosiy menyudasiz.", reply_markup=main_menu)
        await state.finish()        
    else:
        await message.answer("Sizda yakunlanmagan elon joylashtirish holati mavjud. \
Yakunlash uchun quyidagilardan birini tanlang!", reply_markup=confrim_btn)