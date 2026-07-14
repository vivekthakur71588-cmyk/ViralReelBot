import os
import requests
import threading
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8814630740:AAHvGwN4xBiQapbaxq6gYqQFWaqqgARRM8o"
bot = telebot.TeleBot(BOT_TOKEN)

# 🚀 SMART BYPASS: Ye line Railway, Render ya kisi bhi doosre atke huyen container ko forcefully disconnect kar degi!
try:
    print("🧹 Cleaning old active sessions from Railway/Render...")
    bot.remove_webhook()
    # Dynamic conflict breaker trigger
    bot.get_updates(offset=-1, timeout=1)
except Exception as e:
    print("Cleanup notification:", e)

desc_cache = {}

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("ℹ️ Menu"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome = "👋 **Welcome to Viral Reel Downloader!**\n\n📌 Send me any Instagram Reel link directly!"
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: True)
def process_links(message):
    url = message.text
    chat_id = message.chat.id

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Please send a valid Instagram Reel link.")
        return

    status_msg = bot.send_message(chat_id, "⏳ **Please wait... Fetching high speed download link...**", parse_mode="Markdown")

    def api_download_worker():
        try:
            api_url = f"https://api.bhadooo.cc/instagram/v1/adownloader?url={url}"
            response = requests.get(api_url, timeout=15).json()
            
            if response.get("status") and response.get("data"):
                media_data = response["data"][0]
                video_url = media_data.get("url")
                title = media_data.get("caption", "Instagram Reel")
                desc_cache[chat_id] = title
                
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("📄 Get description", callback_data="fetch_desc"))
                
                bot.delete_message(chat_id, status_msg.message_id)
                bot.send_video(chat_id, video_url, caption="📹 **Video Downloaded Successfully!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown", reply_markup=markup)
            else:
                raise Exception("Invalid response")
        except Exception as e:
            bot.edit_message_text("❌ **Download failed!** Server connection error.", chat_id, status_msg.message_id)

    threading.Thread(target=api_download_worker).start()

@bot.callback_query_handler(func=lambda call: call.data == "fetch_desc")
def dispatch_description(call):
    chat_id = call.message.chat.id
    caption = desc_cache.get(chat_id, "⚠️ No description text parsed.")
    bot.send_message(chat_id, f"📝 **Video Caption/Description:**\n\n`{caption}`", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

print("🚀 Anti-conflict bypass system active...")
bot.infinity_polling(skip_pending=True)  # Skip pending updates to prevent crashing
