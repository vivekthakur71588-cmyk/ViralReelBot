import os
import requests
import threading
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8814630740:AAHvGwN4xBiQapbaxq6gYqQFWaqqgARRM8o"
bot = telebot.TeleBot(BOT_TOKEN)

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
    bot.send_message(message.chat.id, "🤖 **Viral Downloader Bot Engine v1.3**\n\n🟢 Status: Fully Active\n⚡ Powered by High-Speed Core Engine", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def process_links(message):
    url = message.text
    chat_id = message.chat.id

    if not (url.startswith("http://") or url.startswith("https://")):
        return

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Please send a valid Instagram Reel link.")
        return

    status_msg = bot.send_message(chat_id, "⏳ **Please wait... Fetching from Premium High-Speed Node...**", parse_mode="Markdown")

    def cobalt_download_worker():
        try:
            # Using stable premium Cobalt dynamic extraction API
            api_url = "https://api.cobalt.tools/api/json"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "url": url,
                "vQuality": "720",
                "isAudioOnly": False,
                "filenamePattern": "classic"
            }
            
            response = requests.post(api_url, json=payload, headers=headers, timeout=20).json()
            
            # Cobalt yields direct tunnel streams under 'url' or nested 'picker' blocks
            video_url = response.get("url")
            
            if not video_url and response.get("status") == "picker":
                picker_items = response.get("picker", [])
                if picker_items:
                    video_url = picker_items[0].get("url")

            if video_url:
                bot.delete_message(chat_id, status_msg.message_id)
                bot.send_video(chat_id, video_url, caption="📹 **Video Downloaded Successfully!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown")
            else:
                raise Exception("Bypass token payload mismatch")
                
        except Exception as e:
            print("Cobalt Node Failure:", e)
            bot.edit_message_text("❌ **Download failed!** Server network is congested. Please re-send the link in a moment.", chat_id, status_msg.message_id)

    threading.Thread(target=cobalt_download_worker).start()

print("🚀 Stable engine framework running...")
bot.infinity_polling(skip_pending=True)
