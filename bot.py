import os
from telegram.ext import ApplicationBuilder, CommandHandler
from pipeline import process
from config import BOT_TOKEN

async def doc(update, context):
    if not context.args:
        await update.message.reply_text("Send YouTube link")
        return

    link = context.args[0]

    await update.message.reply_text("Generating documentary Shorts...")

    process(link)

    await update.message.reply_text("Uploading Shorts...")

    for i in range(4):
        path = f"exports/short_{i}.mp4"
        if os.path.exists(path):
            with open(path, "rb") as v:
                await update.message.reply_video(v)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("doc", doc))

print("Bot running...")
app.run_polling()
