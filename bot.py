import os
import requests
import threading
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8814630740:AAHvGwN4xBiQapbaxq6gYqQFWaqqgARRM8o"
bot = telebot.TeleBot(BOT_TOKEN)

# Forceful session engine reset block
try:
    print("🧹 Detaching any stuck active telegram polling routes...")
    bot.remove_webhook()
    time.sleep(2)
except Exception as e:
    print("Session management note:", e)

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("ℹ️ Menu"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome = "👋 **Welcome to Viral Reel Downloader!**\n\n📌 Send me any Instagram Reel link directly!"
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "ℹ️ Menu")
def show_menu(message):
    bot.send_message(message.chat.id, "🤖 **Viral Downloader Bot Engine v1.2**\n\n🟢 Status: Fully Active", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def process_links(message):
    url = message.text
    chat_id = message.chat.id

    if not (url.startswith("http://") or url.startswith("https://")):
        return

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Please send a valid Instagram Reel link.")
        return

    status_msg = bot.send_message(chat_id, "⏳ **Please wait... Processing link...**", parse_mode="Markdown")

    def api_download_worker():
        try:
            fallback_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            fallback_resp = requests.get(fallback_url, timeout=15).json()
            
            video_url = None
            if "result" in fallback_resp and "video" in fallback_resp["result"]:
                video_url = fallback_resp["result"]["video"].get("url") or fallback_resp["result"]["video"].get("noWatermark")
            elif "result" in fallback_resp:
                video_url = fallback_resp["result"].get("videoUrl")
            
            if not video_url and "url" in fallback_resp:
                video_url = fallback_resp["url"]

            if video_url:
                bot.delete_message(chat_id, status_msg.message_id)
                bot.send_video(chat_id, video_url, caption="📹 **Video Downloaded Successfully!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown")
            else:
                raise Exception("Failed to parse video url path")
        except Exception as e:
            print("Download error:", e)
            bot.edit_message_text("❌ **Download failed!** Server connection timed out. Please try again.", chat_id, status_msg.message_id)

    threading.Thread(target=api_download_worker).start()

print("🚀 Dynamic webhook framework loaded successfully...")
bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
