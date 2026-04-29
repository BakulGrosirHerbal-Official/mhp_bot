import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
MHP_API = "https://mhp-dark-ai.vercel.app/api/ai/ask"
PORT = int(os.environ.get("PORT", 5000))

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 MHP Bot Running!"

def tanya_mhp(pesan, user_name="Sayang"):
    try:
        res = requests.post(MHP_API, json={
            "message": pesan,
            "systemPrompt": f"Kamu MHP Dark AI. User: {user_name}. Jawab singkat ramah."
        }, timeout=90)
        return res.json().get("reply", "😵 Sibuk~")
    except:
        return "😵 MHP sedang sibuk~"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 *MHP Bot siap!*\nChat aja~", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name or "Sayang"
    pesan = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    balasan = tanya_mhp(pesan, user_name)
    if len(balasan) > 4000: balasan = balasan[:4000] + "\n..."
    await update.message.reply_text(balasan)

def run_bot():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    loop.run_until_complete(app.initialize())
    loop.run_until_complete(app.updater.start_polling())
    loop.run_forever()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    flask_app.run(host="0.0.0.0", port=PORT)
