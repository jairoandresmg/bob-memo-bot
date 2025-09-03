# bot.py
import os
import asyncio
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_IDS = [int(x) for x in (os.getenv("TELEGRAM_USER_ID", "").split(",")) if x.strip()]

if not TOKEN or not USER_IDS:
    raise RuntimeError("Faltan variables de entorno TELEGRAM_BOT_TOKEN o TELEGRAM_USER_ID")

bot = Bot(token=TOKEN)
TZ = ZoneInfo("America/Bogota")  # ajusta si necesitas otra zona horaria

async def send_noon_message():
    text = "Hola, es medio día ☀️"
    for chat_id in USER_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            # log mínimo a consola para revisar en Render
            print(f"[ERROR] al enviar a {chat_id}: {e}", flush=True)

async def main():
    # Programar tarea diaria 12:00
    scheduler = AsyncIOScheduler(timezone=TZ)
    scheduler.add_job(send_noon_message, CronTrigger(hour=12, minute=7))
    scheduler.start()

    print("Worker iniciado. Enviará mensaje todos los días a las 12:00 (America/Bogota).", flush=True)

    # Mantener proceso vivo
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())
