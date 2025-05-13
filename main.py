from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater
import os
from dotenv import load_dotenv
from bot.dispatcher import setup_dispatcher

load_dotenv('.env')
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
bot = Bot(token=API_KEY)

# Inisialisasi Updater sekali saja
updater = Updater(bot=bot, use_context=True)
dp = updater.dispatcher
setup_dispatcher(dp)

@app.route(f"/{API_KEY}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return 'ok'

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # Untuk development lokal (polling)
    # updater.start_polling()
    # print('Bot is running locally with polling...')
    # updater.idle()

    # Untuk production (webhook)
    URL = os.getenv('URL')
    webhook_url = f"{URL}/{API_KEY}"
    print(f"🔄 Setting webhook to: {webhook_url}")  # Debugging
    bot.set_webhook(webhook_url)

    app.run(host="0.0.0.0", port=8080)