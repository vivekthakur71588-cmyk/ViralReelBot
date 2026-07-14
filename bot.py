import os
import requests
import threading
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8814630740:AAHvGwN4xBiQapbaxq6gYqQFWaqqgARRM8o"
bot = telebot.TeleBot(BOT_TOKEN)

desc_cache = {}

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("ℹ️ Menu"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome = "👋 **Welcome to Viral Reel Downloader!**\n\n📌 Send me any Instagram Reel or Story link directly!"
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "ℹ️ Menu")
def show_menu(message):
    bot.send_message(message.chat.id, "🤖 **Viral Downloader Bot Engine v1.2**\n\n🟢 Status: Fully Active\n⚡ Multi-API Network Connected", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def process_links(message):
    url = message.text
    chat_id = message.chat.id

    # Strict string filter trigger to bypass button interactions
    if not (url.startswith("http://") or url.startswith("https://")):
        return

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Please send a valid Instagram Reel or Story link.")
        return

    status_msg = bot.send_message(chat_id, "⏳ **Please wait... Processing through High-Speed Node...**", parse_mode="Markdown")

    def api_download_worker():
        try:
            # High-end stable public extraction layer gateway API
            api_url = f"https://api.download.savetube.me/info?url={url}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(api_url, headers=headers, timeout=15).json()
            
            # Check for direct standard video streams or nested source blocks
            video_url = None
            title = "Instagram Media"
            
            if response.get("status") and "data" in response:
                data = response["data"]
                title = data.get("title", "Instagram Media")
                
                # Check different data objects for video links
                if isinstance(data.get("downloadUrl"), str):
                    video_url = data["downloadUrl"]
                elif isinstance(data.get("media"), list) and len(data["media"]) > 0:
                    video_url = data["media"][0].get("url")
                elif isinstance(data.get("stream"), str):
                    video_url = data["stream"]

            if video_url:
                desc_cache[chat_id] = title
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("📄 Get description", callback_data="fetch_desc"))
                
                bot.delete_message(chat_id, status_msg.message_id)
                bot.send_video(chat_id, video_url, caption="📹 **Video Downloaded Successfully!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown", reply_markup=markup)
            else:
                raise Exception("Media link extraction failed")
                
        except Exception as e:
            print("Extraction Log Error:", e)
            # Switch to universal open engine logic fallback mirror if main fails
            try:
                fallback_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
                fallback_resp = requests.get(fallback_url, timeout=15).json()
                video_url = fallback_resp.get("result", {}).get("videoUrl") or fallback_resp.get("url")
                
                if video_url:
                    bot.delete_message(chat_id, status_msg.message_id)
                    bot.send_video(chat_id, video_url, caption="📹 **Video Downloaded via Backup Node!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown")
                    return
            except:
                pass
                
            bot.edit_message_text("❌ **Download failed!** Server connection timed out. Please try sending the link once again.", chat_id, status_msg.message_id)

    threading.Thread(target=api_download_worker).start()

@bot.callback_query_handler(func=lambda call: call.data == "fetch_desc")
def dispatch_description(call):
    chat_id = call.message.chat.id
    caption = desc_cache.get(chat_id, "⚠️ No description text parsed.")
    bot.send_message(chat_id, f"📝 **Video Caption/Description:**\n\n`{caption}`", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

print("🚀 Engine v1.2 successfully loaded...")
bot.infinity_polling(skip_pending=True)
