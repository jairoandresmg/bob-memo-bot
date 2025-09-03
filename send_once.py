# send_once.py
import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_IDS = [int(x) for x in os.getenv("TELEGRAM_USER_ID", "").split(",") if x.strip()]

# Puedes cambiar el texto vía env var sin tocar código
TEXT = os.getenv("MESSAGE_TEXT", "Hola, es medio día ☀️")

if not TOKEN or not USER_IDS:
    raise RuntimeError("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_USER_ID")

async def main():
    bot = Bot(token=TOKEN)
    for chat_id in USER_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=TEXT)
        except Exception as e:
            print(f"[ERROR] Enviando a {chat_id}: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
