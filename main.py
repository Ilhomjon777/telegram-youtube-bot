import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! YouTube videolarini audio yoki video shaklida yuklab olish uchun havolasini yuboring."
    )

# YouTube audio va videosini yuklab olish
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    # Foydalanuvchiga xabar yuborish
    await update.message.reply_text(f"Yuklab olish boshlandi: {url}")

    # YouTube-dan faqat audio yuklab olish uchun sozlamalar
    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',  # Fayl nomi
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # YouTube-dan video yuklab olish uchun sozlamalar
    video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s',  # Fayl nomi
        'noplaylist': True,
        'quiet': True,
    }

    try:
        # YouTube-dan audio yuklab olish
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])
        audio_path = "audio.mp3"

        # YouTube-dan video yuklab olish
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])
        video_path = "video.mp4"

        # Telegram foydalanuvchiga audio va video fayllarni yuborish
        await update.message.reply_audio(audio=open(audio_path, 'rb'))
        await update.message.reply_video(video=open(video_path, 'rb'))

        # Yuklab olingan fayllarni o‘chirish (xotirani tejash uchun)
        os.remove(audio_path)
        os.remove(video_path)

    except Exception as e:
        await update.message.reply_text("Kechirasiz, yuklab olishda xatolik yuz berdi.")

# Asinxron botni ishga tushirish
async def main():
    application = ApplicationBuilder().token("SIZNING_BOT_TOKENINGIZ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("Bot ishga tushdi!")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())  # ✅ Asinxron ishga tushirish

