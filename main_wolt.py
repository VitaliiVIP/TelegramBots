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
    await message.answer(f"<b>Hello, {message.from_user.first_name}!</b>\nI am bot, who will help you with getting an account. Before you contact our manager, let's answer some questions.\nAre you ready to start?\n\n<i>(Click \"Start\" below this message)</i>", parse_mode="HTML", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "start")
async def process_start(callback_query: CallbackQuery):
    user_data[callback_query.from_user.id] = {}
    await bot.send_message(callback_query.from_user.id, "What is your full name?")
    await callback_query.answer()

@dp.message(lambda message: message.from_user.id in user_data and "name" not in user_data[message.from_user.id])
async def get_name(message: Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("In what city do you want an account?\n<i>(You can choose several)</i>", parse_mode="HTML")

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
    await bot.send_message(callback_query.from_user.id, "What country are you from?\n(Before you came to Finland)")
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
        [InlineKeyboardButton(text="🤷‍♂️ I don't know whatis it", callback_data="business_unknown")]
    ])
    await message.answer("Do you have Business ID?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "business_unknown")
async def process_business_unknown(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["BID"] = "🤷‍♂️"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I've checked", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id, "Please, check Truster.fi for getting info", reply_markup=keyboard)
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
    await bot.send_message(callback_query.from_user.id, "That's good! Are you ready to read an instruction?", reply_markup=keyboard)
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
    await bot.send_message(callback_query.from_user.id, "We would recommend you to get Business ID, otherwise you will not be able to work in Foodora (only in Wolt).", reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "read_instructions")
async def process_read_instructions(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I've read", callback_data="confirm_read")]
    ])
    message_text = ("<b>❗ INSTRUCTION ❗</b>\n\n"
                    "READ IT CAREFULLY!\n\n"
                    "Since we started our group we connected 12 accounts and now our group is growing, and we decided to make an Instruction for new people:\n\n"
                    "<b>1.</b> We are the group that connects people who are looking for the account with owners.\n\n"
                    "<b>2.</b> We take a fixable amount from each account every month. Depends on the location of the account we take 50-99 euros (sum is already included in written cost).\n\n"
                    "<b>3.</b> Since we start our group a few people decided to trick us and not pay any money after getting the account. These people lost access to the accounts because we contacted owners. So we decided to take 0.01€ for getting all your personal information (When you send it in Bank app or MobilePay, we see your account's details).\n\n"
                    "<b>4.</b> At the end of the first workday, you must pay 20€ as a guarantee, that you will pay us further.\n\n"
                    "We hoping on a nice partnership with you 😊")
    await bot.send_message(callback_query.from_user.id, message_text, parse_mode='HTML', reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "confirm_read")
async def process_read(callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = callback_query.from_user.id
    if user_id in user_data:
        data = user_data[user_id]
        name = data.get("name", "Didn't write")
        city = data.get("city", "Didn't write")
        transport = data.get("transport", "Didn't write").replace("transport_", "").capitalize()
        country = data.get("country", "Didn't write")
        phone = data.get("phone", "Didn't provide")
        b_id=data.get("BID", "Didn't provide")
        message_text = (f"Name: {name}\n"
                        f"City: {city}\n"
                        f"Vehicle Type: {transport}\n"
                        f"Business ID: {b_id}\n"
                        f"Country: {country}\n"
                        f"Phone: {phone}\n"
                        f"Telegram ID: @{username if username else 'X'}")

        group_chat_id = '@ushdhdhdisj52'
        await bot.send_message(group_chat_id, message_text)

    await bot.send_message(user_id, "Managers got your information!\n\nContact one of them:\n@wolt_ac\n@johnywellman\n\n<i>(Click on one of them for open chat)</i>", parse_mode="HTML")
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
