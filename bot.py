from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram.request import HTTPXRequest
import pymongo

client = pymongo.MongoClient("mongodb://vibeossupport_db_user:T5MgK81nVoZk50bc@ac-kryc93r-shard-00-00.ibuc0rv.mongodb.net:27017,ac-kryc93r-shard-00-01.ibuc0rv.mongodb.net:27017,ac-kryc93r-shard-00-02.ibuc0rv.mongodb.net:27017/?ssl=true&replicaSet=atlas-fmry30-shard-0&authSource=admin&appName=Cluster0")
db = client["vibeOS"]

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


request = HTTPXRequest(
    connect_timeout=30,
    read_timeout=60,
    write_timeout=60,
    pool_timeout=30
)

app = (
    ApplicationBuilder()
    .token("8795425415:AAHOnBoDrUc_IaA3UuGsAlRvcOuUBwTIfhY")
    .request(request)
    .build()
)

app.add_handler(
    MessageHandler(filters.PHOTO, photo_handler)
)

print("Bot starting...")
app.run_polling()