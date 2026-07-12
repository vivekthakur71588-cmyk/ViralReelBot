import os
import telebot
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# 1. Dummy Health Server Render ko khush rakhne ke liye
def run_health_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"📡 Dummy web server running on port {port}...")
    server.serve_forever()

# Background thread mein server chalayein
threading.Thread(target=run_health_server, daemon=True).start()

# 2. Actual Telegram Bot Engine
BOT_TOKEN = "8814630740:AAH5NZuguoz6mnVjCy-l5kq7F_ETQ17Pvnw"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Aapka bot ab 100% active aur live ho chuka hai!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "🔍 Link received: " + message.text)

print("🚀 Bot engine successfully triggered and active...")
bot.infinity_polling()
