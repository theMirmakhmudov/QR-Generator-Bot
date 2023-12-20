import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from config import token
from aiogram.types import BufferedInputFile

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Assalomu Aleykum Xurmatli <b>{message.from_user.full_name}</b> \nQR botimizga xush kelibsiz!",
        parse_mode=ParseMode.HTML)
    print(message.from_user.id)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(f"""
<b>Sizga qanday yordam bera olaman?
Qayta boshlash uchun : /start</b>
    """, parse_mode="HTML")


@dp.message(Command("qr"))
async def cmd_qr(message: types.Message):
    await message.answer("<b>Ma'lumotlaringizni kiriting:\nNamuna : Name Surname Email Phone Number</b>",
                         parse_mode="HTML")
    await message.answer("<b>Ps: har bir ma'lumotingizdan keyin probel tashlang</b>", parse_mode="HTML")

    @dp.message()
    async def qr(message: types.Message):
        text = message.text
        text2 = text.split(" ")
        import qrcode
        first_name = text2[0]
        last_name = text2[1]
        email = text2[2]
        phone_number = text2[3]

        vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{last_name};{first_name};;;\nFN:{first_name}\nEMAIL;TYPE=INTERNET:{email}\nTEL;TYPE=CELL:{phone_number}\nEND:VCARD"

        img = qrcode.make(vcard)

        img.save("user.png")

        file_ids = []

        with open("user.png", "rb") as image_from_buffer:
            result = await message.answer_photo(
                BufferedInputFile(
                    image_from_buffer.read(),
                    filename="user.png"
                ), caption=f"<b>Name: {text2[0]}\nSurname: {text2[1]}\nEmail: {text2[2]}\nPhone Number: {text2[3]}</b>",
                parse_mode="HTML")

            file_ids.append(result.photo[-1].file_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
