import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

TOKEN = "8166513060:AAFZDAy1MBeYgkDpQVU56zEsmdN01ooft1k"
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
    await bot.send_message(callback_query.from_user.id, "What is your name?")
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
    await bot.send_message(callback_query.from_user.id, "Where are you from?\n(Before you came to Finland)")
    await callback_query.answer()


@dp.message(lambda message: message.from_user.id in user_data and "country" not in user_data[message.from_user.id])
async def get_country(message: Message):
    user_data[message.from_user.id]["country"] = message.text
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Yes", callback_data="business_yes")],
        [InlineKeyboardButton(text="❌ No", callback_data="business_no")],
        [InlineKeyboardButton(text="🤷‍♂️ I don't know what is it", callback_data="business_unknown")]
    ])
    await message.answer("Do you have Business ID?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in ["business_yes", "business_no", "business_unknown"])
async def process_business_id(callback_query: CallbackQuery):
    if callback_query.data == "business_unknown":
        await bot.send_message(callback_query.from_user.id, "Please, check Truster.fi for getting info")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I've read", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id, "<b>              ❗       INSTRUCTION       ❗\n\nREAD IT CAREFULLY!</b>\n\nSince we started our group we connected 12 accounts and now our group is growing, and we decided to make an Instruction for new people:\n\n<b>1.</b> We are the group that connects people who are looking for the account with owners.\n\n<b>2.</b> We take fixable amount from each account every month. Depends on the location of the account we take 50-99 euros (sum is already included in written cost).\n\n<b>3.</b> Since we start our group few people decided to trick us and not pay any money after getting the account. This people lost access to the accounts, because we contacted owners. So we decided to take 0.01€ for getting all your personal information (When you send it in Bank app or MobilePay, we see your account's details).\n\n<b>4.</b> In the end of the first workday you must pay 20€ as a guarantee, that you will pay to us further.\n\nWe hoping on nice partnership with you 😊",
                           parse_mode='HTML', reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "read_instructions")
async def process_read(callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = callback_query.from_user.id
    if user_id in user_data:
        data = user_data[user_id]
        name = data.get("name", "Didn't write")
        city = data.get("city", "Didn't write")
        transport = data.get("transport", "Didn't write").replace("transport_", "").capitalize()
        country = data.get("country", "Didn't write")
        message_text = (f"Name: {name}\n"
                        f"City: {city}\n"
                        f"Vehicle Type: {transport}\n"
                        f"Country: {country}\n"
                        f"Telegram ID: @{username if username else 'X'}")

        group_chat_id = '@ushdhdhdisj52'
        await bot.send_message(group_chat_id, message_text)

    await bot.send_message(user_id, "Managers got your information!\n\nContact one of them:\n@wolt_ac\n@johnywellman\n(Click on one of them for open chat)")
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())