import telebot
import os

# Railway variables se token uthayega, agar nahi mila toh hardcoded use karega
BOT_TOKEN = os.getenv("BOT_TOKEN", "8814630740:AAEcQJICbiSlxAbJc1Y9eB-U2OFPbERVNe4")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Aapka bot ab 100% active aur live ho chuka hai!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "🔍 Link received: " + message.text)

print("🚀 Bot engine successfully triggered and active...")
bot.infinity_polling()
