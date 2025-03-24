import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

TOKEN = ""
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
user_data = {}


@dp.message(Command("start"))
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start", callback_data="start")]
    ])
    await message.answer(
        f"<b>Hello, {message.from_user.first_name}!</b>\nI am bot, who will help you with getting an account. Before you contact our manager, let's answer some questions.\nAre you ready to start?\n\n<i>(Click \"Start\" below this message)</i>",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "start")
async def process_start(callback_query: CallbackQuery):
    user_data[callback_query.from_user.id] = {}
    await bot.send_message(callback_query.from_user.id, "What is your full name?")
    await callback_query.answer()


@dp.message(lambda message: message.from_user.id in user_data and "name" not in user_data[message.from_user.id])
async def get_name(message: Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Finland", callback_data="country_finland")],
        [InlineKeyboardButton(text="Great Britain", callback_data="country_gb")]
    ])
    await message.answer("In what country do you want an account?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in ["country_finland", "country_gb"])
async def process_country(callback_query: CallbackQuery):
    countries = {
        "country_finland": "Finland",
        "country_gb": "Great Britain"
    }
    user_data[callback_query.from_user.id]["current_country"] = countries[callback_query.data]
    await bot.send_message(callback_query.from_user.id,
                           "In what city do you want an account?\n<i>(You can choose several)</i>", parse_mode="HTML")
    await callback_query.answer()


@dp.message(lambda message: message.from_user.id in user_data and "city" not in user_data[message.from_user.id])
async def get_city(message: Message):
    user_data[message.from_user.id]["city"] = message.text
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Car", callback_data="transport_car")],
        [InlineKeyboardButton(text="🚲 Bike/E-bike", callback_data="transport_bike")],
        [InlineKeyboardButton(text="🚗🚲 Both are suitable", callback_data="transport_both")]
    ])
    await message.answer("Account with what type of transport do you need?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in ["transport_car", "transport_bike", "transport_both"])
async def process_transport(callback_query: CallbackQuery):
    user_data[callback_query.from_user.id]["transport"] = callback_query.data
    await bot.send_message(callback_query.from_user.id,
                           "What country are you from?\n(Before you came to the current living place)")
    await callback_query.answer()


@dp.message(lambda message: message.from_user.id in user_data and "country" not in user_data[message.from_user.id])
async def get_country(message: Message):
    user_data[message.from_user.id]["country"] = message.text
    await message.answer("What is your phone number?")


@dp.message(lambda message: message.from_user.id in user_data and "phone" not in user_data[message.from_user.id])
async def get_phone(message: Message):
    user_data[message.from_user.id]["phone"] = message.text
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Yes", callback_data="business_yes")],
        [InlineKeyboardButton(text="❌ No", callback_data="business_no")],
        [InlineKeyboardButton(text="🤷‍♂️ I don't know whatis it", callback_data="business_unknown")],
        [InlineKeyboardButton(text="🚫️ I am not from Finland", callback_data="business_not_needed")]
    ])
    await message.answer("Do you have Business ID?\n <i>(Question is only for clients from Finland)</i>",
                         parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "business_unknown")
async def process_business_unknown(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["BID"] = "🤷‍♂️"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I've checked", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id, "Please, check Truster.fi for getting info",
                           reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "business_yes")
async def process_business_yes(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["BID"] = "✅"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yes, sure!", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id, "That's good! Are you ready to read an instruction?",
                           reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "business_no")
async def process_business_no(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["BID"] = "❌"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Okay, I understand", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id,
                           "We would recommend you to get Business ID, otherwise you will not be able to work in Foodora (only in Wolt).",
                           reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "business_not_needed")
async def process_business_yes(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["BID"] = "🇬🇧"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yes, sure!", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id, "Okay. Are you ready to read an instruction?",
                           reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "read_instructions")
async def process_read_instructions(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I've read", callback_data="confirm_read")]
    ])
    message_text = ("<b>❗ INSTRUCTION ❗</b>\n\n"
                    "READ IT CAREFULLY!\n\n"
                    "<b>Welcome to our group!</b> We connect individuals seeking accounts with verified owners. Please read the following carefully before proceeding.\n\n"

                    "<b>1️⃣ Payment Structure</b\n>"
                    "Each account involves two types of payments:\n"

                    "🔹 <b>Owner’s Fee</b> – Paid directly to the account owner.\n"
                    "🔹 <b>Group Fee</b> – Paid to our group.\n"

                    "📌 <b>Finland:</b>\n"

                    "Owner’s Fee – A fixed amount or percentage.\n"
                    "Group Fee – €50-€99/month.\n"
                    "📌 <b>UK:</b>\n"
                    "Owner’s Fee – £80-£100 per week.\n"
                    "Group Fee – £5-£10 per week.\n\n"

                    "<b>2️⃣ Commitment & Account Changes</b>\n"
                    "🔸 Once you agree with an owner, you must use the account for at least one month before requesting a change.\n"
                    "🔸 If you wish to switch accounts earlier, you must pay one month’s group fee for a replacement.\n\n"

                    "<b>3️⃣ Payment Rules</b>\n"
                    "🔹 Finland: Group payments are due on the 1st of each month.\n"
                    "🔹 UK: Group payments are due weekly on the agreed payment day.\n"
                    "🔹 If delayed by more than 14 days (Finland and UK), access to the account will be revoked.\n"
                    "🔹 If you start mid-month (Finland) or mid-week (UK), your fee is calculated based on the remaining days.\n\n"

                    "<b>4️⃣ Security & Guarantee</b>\n"
                    "🔸 Due to past issues with non-payment, we require a €0.01/£0.01 transfer to verify your identity.\n"
                    "🔸 On your first workday, you must pay €20 (Finland) or £5 (UK) as a guarantee for future payments.\n\n"

                    "<b>⚠️ Failure to follow these rules may result in account suspension. ⚠️</b>\n\n"

                    "<b>We look forward to a successful partnership with you! 😊</b>"
                    )
    await bot.send_message(callback_query.from_user.id, message_text, parse_mode='HTML', reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "confirm_read")
async def process_read(callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = callback_query.from_user.id
    if user_id in user_data:
        data = user_data[user_id]
        name = data.get("name", "Didn't write")
        account_country = data.get("current_country", "Didn't write")
        city = data.get("city", "Didn't write")
        transport = data.get("transport", "Didn't write").replace("transport_", "").capitalize()
        country = data.get("country", "Didn't write")
        phone = data.get("phone", "Didn't provide")
        b_id = data.get("BID", "Didn't provide")
        if b_id == "🇬🇧":
            message_text = (f"Name: {name}\n"
                            f"Country: {account_country}\n"
                            f"City: {city}\n"
                            f"Vehicle Type: {transport}\n"
                            f"From: {country}\n"
                            f"Phone: {phone}\n"
                            f"Telegram ID: @{username if username else 'X'}")

            group_chat_id = '@ushdhdhdisj52'
            await bot.send_message(group_chat_id, message_text)
            await bot.send_message(user_id,
                                   "<b>Check your application:</b>\n\n"
                                   f"<b>Name:</b> {name}\n"
                                   f"<b>Country:</b> {account_country}\n"
                                   f"<b>City:</b> {city}\n"
                                   f"<b>Vehicle Type:</b> {transport}\n"
                                   f"<b>From:</b> {country}\n"
                                   f"<b>Phone:</b> {phone}\n\n"
                                   "Managers are ready to chat with you!\n\nContact one of them and send this message to him:\n@wolt_ac\n@johnywellman\n\n<i>(Click on one of them for open chat)</i>",
                                   parse_mode="HTML")
        else:
            message_text = (f"Name: {name}\n"
                            f"Country: {account_country}\n"
                            f"City: {city}\n"
                            f"Vehicle Type: {transport}\n"
                            f"Business ID: {b_id}\n"
                            f"From: {country}\n"
                            f"Phone: {phone}\n"
                            f"Telegram ID: @{username if username else 'X'}")

            group_chat_id = '@ushdhdhdisj52'
            await bot.send_message(group_chat_id, message_text)
            await bot.send_message(user_id,
                                   "<b>Check your application:</b>\n\n"
                                   f"<b>Name:</b> {name}\n"
                                   f"<b>Country:</b> {account_country}\n"
                                   f"<b>City:</b> {city}\n"
                                   f"<b>Vehicle Type:</b> {transport}\n"
                                   f"<b>Business ID:</b> {b_id}\n"
                                   f"<b>From:</b> {country}\n"
                                   f"<b>Phone:</b> {phone}\n\n"
                                   "Managers are ready to chat with you!\n\nContact one of them and send this message to him:\n@wolt_ac\n@johnywellman\n\n<i>(Click on one of them for open chat)</i>",
                                   parse_mode="HTML")

    await callback_query.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())