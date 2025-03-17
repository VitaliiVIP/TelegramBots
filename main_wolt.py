import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

# Твой токен бота
TOKEN = "8166513060:AAFZDAy1MBeYgkDpQVU56zEsmdN01ooft1k"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранение данных пользователей
user_data = {}


# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start", callback_data="start")]
    ])
    await message.answer("Привет! Нажмите кнопку, чтобы начать.", reply_markup=keyboard)


# Обработка нажатия кнопки Start
@dp.callback_query(lambda c: c.data == "start")
async def process_start(callback_query: CallbackQuery):
    user_data[callback_query.from_user.id] = {}
    await bot.send_message(callback_query.from_user.id, "Как вас зовут?")
    await callback_query.answer()


# Получение имени
@dp.message(lambda message: message.from_user.id in user_data and "name" not in user_data[message.from_user.id])
async def get_name(message: Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("В каком городе вы хотите аккаунт?")


# Получение города
@dp.message(lambda message: message.from_user.id in user_data and "city" not in user_data[message.from_user.id])
async def get_city(message: Message):
    user_data[message.from_user.id]["city"] = message.text
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Машина", callback_data="transport_car")],
        [InlineKeyboardButton(text="🚲 Велосипед", callback_data="transport_bike")],
        [InlineKeyboardButton(text="🚗🚲 И то, и то", callback_data="transport_both")]
    ])
    await message.answer("На каком транспорте вы готовы работать?", reply_markup=keyboard)


# Обработка выбора транспорта
@dp.callback_query(lambda c: c.data in ["transport_car", "transport_bike", "transport_both"])
async def process_transport(callback_query: CallbackQuery):
    user_data[callback_query.from_user.id]["transport"] = callback_query.data
    await bot.send_message(callback_query.from_user.id, "Откуда вы родом?")
    await callback_query.answer()


# Получение страны
@dp.message(lambda message: message.from_user.id in user_data and "country" not in user_data[message.from_user.id])
async def get_country(message: Message):
    user_data[message.from_user.id]["country"] = message.text
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="business_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="business_no")],
        [InlineKeyboardButton(text="🤷‍♂️ Я не знаю", callback_data="business_unknown")]
    ])
    await message.answer("У вас есть бизнес ID?", reply_markup=keyboard)


# Обработка бизнес ID
@dp.callback_query(lambda c: c.data in ["business_yes", "business_no", "business_unknown"])
async def process_business_id(callback_query: CallbackQuery):
    if callback_query.data == "business_unknown":
        await bot.send_message(callback_query.from_user.id, "Пожалуйста, проверьте Truster.fi.")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I've read", callback_data="read_instructions")]
    ])
    await bot.send_message(callback_query.from_user.id, "<b>Here is the instruction.\n READ IT CAREFULLY!</b>\n\nSince we started our group we connected 6 accounts and now our group is growing, and we decided to make an Instruction for new people:\n\n<b>1.</b> We are the group that connects people who are looking for the account with owners.\n\n<b>2.</b> We take fixable amount from each account every month. Depends on the location of the account we take 50-99 euros (sum is already included in written cost).\n\n3. Since we start our group few people decided to trick us and not pay any money after getting the account. This people lost access to the accounts, because we contacted owners. So we decided to take 0.01€ for getting all your personal information (When you send it in Bank app or MobilePay, we see your account's details).\n\n4. In the end of the first workday you must pay 20€ as a guarantee, that you will pay to us further.\n\nWe hoping on nice partnership with you 😊",
                           parse_mode='HTML', reply_markup=keyboard)
    await callback_query.answer()


# Подтверждение прочтения инструкции
# Подтверждение прочтения инструкции
# Подтверждение прочтения инструкции
@dp.callback_query(lambda c: c.data == "read_instructions")
async def process_read(callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = callback_query.from_user.id
    # Проверяем, находимся ли мы в данных пользователя
    if user_id in user_data:
        data = user_data[user_id]
        name = data.get("name", "Не указано")
        city = data.get("city", "Не указано")
        transport = data.get("transport", "Не указано").replace("transport_", "").capitalize()
        country = data.get("country", "Не указано")
        # Форматируем сообщение, включая Telegram ID пользователя
        message_text = (f"Имя: {name}\n"
                        f"City: {city}\n"
                        f"Vehicle Type: {transport}\n"
                        f"Country: {country}\n"
                        f"Telegram ID: @{username if username else 'X'}")

        # Отправляем сообщение в группу
        group_chat_id = '@ushdhdhdisj52'  # Замените на вашу группу
        await bot.send_message(group_chat_id, message_text)

    # Отправляем пользователю подтверждение
    await bot.send_message(user_id, "Managers got your information!\n\nContact one of them: @wolt_ac, @johnywellman")
    await callback_query.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())