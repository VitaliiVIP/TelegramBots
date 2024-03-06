import os
import telebot
from telebot import types
from googletrans import Translator, LANGUAGES

BOT_TOKEN = '7021310891:AAFCULpbm3uN39sXW5km20X-91T4ycOf3kg'
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()
facts = [
    "Fact 1: The most widely spoken language in the world is English.",
    "Fact 2: There are over 7,000 languages spoken in the world today.",
    "Fact 3: The oldest written language was Sumerian.",
]
subscribed_users={}

user_language_choices = {}
user_source_language_choices = {}

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)  # one_time_keyboard=True makes the keyboard disappear after use
        # Replace these with the flags or options you want to provide
        flag1 = types.KeyboardButton("🇬🇧 United\nKingdom")
        flag2 = types.KeyboardButton("🇫🇷 France")
        flag3 = types.KeyboardButton("🇩🇪 Germany")
        flag4 = types.KeyboardButton("🇫🇮 Finland")
        flag5 = types.KeyboardButton("🇪🇸 Spain")
        flag6 = types.KeyboardButton("🇮🇳 India")
        flag7 = types.KeyboardButton("🇮🇹 Italy")
        flag8 = types.KeyboardButton("🇯🇵 Japan")
        flag9 = types.KeyboardButton("🇰🇷 South Korea")
        flag10 = types.KeyboardButton("🇸🇪 Sweden")
        flag11 = types.KeyboardButton("🇷🇴 Romania")
        flag12 = types.KeyboardButton("🇻🇳 Vietnam")
        flag13 = types.KeyboardButton("🇺🇦 Ukraine")
        flag14 = types.KeyboardButton("🇨🇳 China")
        flag15 = types.KeyboardButton("🇷🇺 Russia")
        flag16 = types.KeyboardButton("🇱🇹 Lithuania")
        flag17 = types.KeyboardButton("🇭🇷 Croatia")
        flag18 = types.KeyboardButton("🇧🇾 Belarus")
        flag19 = types.KeyboardButton("🇪🇪 Estonia")
        flag20 = types.KeyboardButton("🇱🇻 Latvia")
        flag21 = types.KeyboardButton("🇰🇿 Kazahstan")
        flag22 = types.KeyboardButton("🇬🇷 Greece")
        markup.add(flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, flag9, flag10, flag11, flag12, flag13, flag14, flag15, flag16, flag17, flag18, flag19, flag20, flag22, flag21)
        user_first_name = message.from_user.first_name
        bot.send_message(message.chat.id, f"Hello, <b>{user_first_name}</b>, I am Bot-Translator! Please, choose the language (use menu).\nYou can use any language as source and switch between destination languages when you want.", reply_markup=markup, parse_mode="HTML")
@bot.message_handler(commands=['speclang'])
def specify(message):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)  # one_time_keyboard=True makes the keyboard disappear after use
        flag1 = types.KeyboardButton("🇬🇧 United\nKingdom")
        flag2 = types.KeyboardButton("🇫🇷 France")
        flag3 = types.KeyboardButton("🇩🇪 Germany")
        flag4 = types.KeyboardButton("🇫🇮 Finland")
        flag5 = types.KeyboardButton("🇪🇸 Spain")
        flag6 = types.KeyboardButton("🇮🇳 India")
        flag7 = types.KeyboardButton("🇮🇹 Italy")
        flag8 = types.KeyboardButton("🇯🇵 Japan")
        flag9 = types.KeyboardButton("🇰🇷 South Korea")
        flag10 = types.KeyboardButton("🇸🇪 Sweden")
        flag11 = types.KeyboardButton("🇷🇴 Romania")
        flag12 = types.KeyboardButton("🇻🇳 Vietnam")
        flag13 = types.KeyboardButton("🇺🇦 Ukraine")
        flag14 = types.KeyboardButton("🇨🇳 China")
        flag15 = types.KeyboardButton("🇷🇺 Russia")
        flag16 = types.KeyboardButton("🇱🇹 Lithuania")
        flag17 = types.KeyboardButton("🇭🇷 Croatia")
        flag18 = types.KeyboardButton("🇧🇾 Belarus")
        flag19 = types.KeyboardButton("🇪🇪 Estonia")
        flag20 = types.KeyboardButton("🇱🇻 Latvia")
        flag21 = types.KeyboardButton("🇰🇿 Kazahstan")
        flag22 = types.KeyboardButton("🇬🇷 Greece")
        markup.add(flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, flag9, flag10, flag11, flag12, flag13, flag14, flag15, flag16, flag17, flag18, flag19, flag20, flag21, flag22)

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    chat_id = message.chat.id
    if message.text in ["🇬🇧 United\nKingdom", "🇫🇷 France", "🇩🇪 Germany", "🇫🇮 Finland", "🇪🇸 Spain", "🇮🇳 India", "🇮🇹 Italy", "🇯🇵 Japan", "🇰🇷 South Korea", "🇸🇪 Sweden", "🇷🇴 Romania", "🇻🇳 Vietnam", "🇺🇦 Ukraine", "🇨🇳 China", "🇱🇹 Lithuania", "🇷🇺 Russia", "🇭🇷 Croatia", "🇧🇾 Belarus", "🇪🇪 Estonia", "🇱🇻 Latvia", "🇰🇿 Kazahstan", "🇬🇷 Greece"]:
        # Map the flag to a language code
        flag_to_lang = {"🇬🇧 United\nKingdom": "en", "🇫🇷 France": "fr", "🇩🇪 Germany": "de", "🇫🇮 Finland": "fi", "🇪🇸 Spain": "es", "🇮🇳 India" : "hi", "🇮🇹 Italy": "it", "🇯🇵 Japan": "ja", "🇰🇷 South Korea": "ko", "🇸🇪 Sweden": "sv", "🇷🇴 Romania": "ro", "🇻🇳 Vietnam": "vi", "🇺🇦 Ukraine": "uk", "🇨🇳 China": "zh-CN", "🇱🇹 Lithuania": 'lt', "🇷🇺 Russia": "ru", "🇭🇷 Croatia": "hr", "🇧🇾 Belarus": "be", "🇪🇪 Estonia": "ee", "🇱🇻 Latvia": "lv", "🇰🇿 Kazahstan": "kk", "🇬🇷 Greece": "el"  }
        user_language_choices[chat_id] = flag_to_lang[message.text]
        bot.reply_to(message, f"Language set to <b>{user_language_choices[chat_id]}</b>. Please send the text you want to translate.", parse_mode='HTML')
    elif chat_id in user_language_choices:
        try:
            # Translate the message to the selected language
            dest_lang = user_language_choices[chat_id]
            translated_text = translator.translate(message.text, dest=dest_lang).text
            bot.reply_to(message, translated_text)
        except Exception as e:
            bot.reply_to(message, "Error: Unable to translate the message.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
