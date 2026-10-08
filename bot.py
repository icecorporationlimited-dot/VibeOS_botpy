import os

import pymongo
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram.request import HTTPXRequest


# =========================
# Environment Variables
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not MONGO_URL:
    raise RuntimeError("MONGO_URL is missing")


# =========================
# MongoDB
# =========================

client = pymongo.MongoClient(MONGO_URL)

db = client["vibeOS"]


# =========================
# Telegram Handler
# =========================

async def photo_handler(update: Update, context):
    photo = update.message.photo[-1].file_id
    user_id = update.message.from_user.id

    db.users.update_one(
        {"telegram_id": str(user_id)},
        {
            "$push": {"photos": photo},
            "$setOnInsert": {"vibe": "baddie"}
        },
        upsert=True
    )

    await update.message.reply_text(
        "Photo mil gayi! Factory me bhej di. Aura Score ban raha hai..."
    )


# =========================
# Telegram Request
# =========================

request = HTTPXRequest(
    connect_timeout=30,
    read_timeout=60,
    write_timeout=60,
    pool_timeout=30
)


# =========================
# Bot
# =========================

app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .request(request)
    .build()
)

app.add_handler(
    MessageHandler(filters.PHOTO, photo_handler)
)


print("Bot starting...")

app.run_polling()
