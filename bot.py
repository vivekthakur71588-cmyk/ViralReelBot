import os
import time
import requests
import threading
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

BOT_TOKEN = "8814630740:AAH5NZuguoz6mnVjCy-l5kq7F_ETQ17Pvnw"
bot = telebot.TeleBot(BOT_TOKEN)

# Temporary cache to store descriptions for the inline button
desc_cache = {}

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("ℹ️ Menu"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome = "👋 **Welcome to Viral Reel Downloader!**\n\n🎯 **100% Free & Unlimited Mode Active**\n📌 Send me any Instagram Reel, TikTok Video, or Pinterest Image link directly!"
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "ℹ️ Menu")
def show_menu(message):
    bot.send_message(message.chat.id, "🤖 **Viral Downloader Bot Engine v1.0**\n\n🟢 Status: Fully Active\n⚡ Features: Free Multi-Platform Downloading", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def process_links(message):
    url = message.text
    chat_id = message.chat.id

    if not any(x in url for x in ["instagram.com", "pinterest.com", "pin.it", "tiktok.com"]):
        bot.reply_to(message, "❌ Invalid Link! Supported: Instagram, TikTok, Pinterest.")
        return

    # 1. Action Layer: "Please wait..." Status message triggers
    status_msg = bot.send_message(chat_id, "⏳ **Please wait... Extracting free download links...**", parse_mode="Markdown")

    def core_download_engine():
        try:
            # Setup custom button layout
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📄 Get description", callback_data="fetch_desc"))

            # --- PINTEREST HANDLER ---
            if "pinterest.com" in url or "pin.it" in url:
                ydl_opts = {'format': 'best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    media_url = info.get('url')
                    title = info.get('title', 'Pinterest Media')
                    desc_cache[chat_id] = title
                    
                    bot.delete_message(chat_id, status_msg.message_id)
                    if info.get('ext') == 'mp4' or '.mp4' in media_url:
                        bot.send_video(chat_id, media_url, caption="📌 **Pinterest Video Downloaded!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown", reply_markup=markup)
                    else:
                        bot.send_photo(chat_id, media_url, caption="📌 **Pinterest Photo Downloaded!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown", reply_markup=markup)

            # --- INSTAGRAM & TIKTOK HANDLER ---
            else:
                # Target path inside current directory
                out_filename = f"video_{chat_id}_{int(time.time())}.mp4"
                ydl_opts = {
                    'outtmpl': out_filename,
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'quiet': True,
                    'merge_output_format': 'mp4'
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', info.get('description', 'No caption available.'))
                    desc_cache[chat_id] = video_title

                bot.delete_message(chat_id, status_msg.message_id)
                
                # Send downloaded video directly to the chat interface
                with open(out_filename, 'rb') as video_file:
                    bot.send_video(chat_id, video_file, caption="📹 **Video Downloaded Successfully!**\n\n⚡ _Via @ViralReelDlBot_", parse_mode="Markdown", reply_markup=markup)
                
                # Clean up server space instantly after sending
                if os.path.exists(out_filename):
                    os.remove(out_filename)

        except Exception as e:
            print("Download Engine Failure Log:", e)
            try:
                bot.delete_message(chat_id, status_msg.message_id)
            except:
                pass
            bot.send_message(chat_id, "❌ **Download failed!** Server could not bypass this link structure or the video is private.")

    threading.Thread(target=core_download_engine).start()

@bot.callback_query_handler(func=lambda call: call.data == "fetch_desc")
def dispatch_description(call):
    chat_id = call.message.chat.id
    caption = desc_cache.get(chat_id, "⚠️ No title or caption embedded in this file structure.")
    bot.send_message(chat_id, f"📝 **Video Caption/Description:**\n\n`{caption}`", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

print("🚀 Free Unlimited Downloader active...")
bot.infinity_polling()
