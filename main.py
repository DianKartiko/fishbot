from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher
import os 

API_KEY = os.getenv('API_KEY')

dp = Dispatcher(API_KEY, None, use_context=True)

app = Flask(__name__)

@app.route(f"/{API_KEY}", methods=["POST"])
def webhook():
    """Endpoint untuk menerima update dari Telegram"""
    update = Update.de_json(request.get_json(force=True), API_KEY)
    dp.process_update(update)
    return 'ok'

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    URL = os.getenv('URL')
    webhook_url = f"{URL}/{API_KEY}"
    print(f"🔄 Setting webhook to: {webhook_url}")  # Debugging
    API_KEY.set_webhook(webhook_url)
    
    # Jalankan Flask
    port = int(os.environ.get("PORT", 8080))  # Fly.io default: 8080
    app.run(host="0.0.0.0", port=8080)