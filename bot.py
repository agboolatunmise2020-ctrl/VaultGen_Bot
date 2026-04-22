import telebot
import secrets
import string
from telebot import types

API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

user_prefs = {}

def gen_pass(length, level):
    chars = string.ascii_letters + string.digits
    if level == "high":
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("8 Chars", callback_data="len_8"),
               types.InlineKeyboardButton("12 Chars", callback_data="len_12"),
               types.InlineKeyboardButton("16 Chars", callback_data="len_16"))
    bot.send_message(message.chat.id, "🔐 Choose password length:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('len_'))
def set_len(call):
    user_prefs[call.message.chat.id] = int(call.data.split('_')[1])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Standard (Alphanumeric)", callback_data="lvl_std"),
               types.InlineKeyboardButton("High (With Symbols)", callback_data="lvl_high"))
    bot.edit_message_text("Select security level:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lvl_'))
def finalize(call):
    length = user_prefs.get(call.message.chat.id, 12)
    level = call.data.split('_')[1]
    password = gen_pass(length, level)
    
    res = f"✅ Your Secure Password:\n`{password}`\n\n(Tap to copy)"
    bot.edit_message_text(res, call.message.chat.id, call.message.message_id, parse_mode="MarkdownV2")

bot.polling()
