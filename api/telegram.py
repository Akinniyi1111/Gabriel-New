from fastapi import FastAPI, Request
from telebot import TeleBot, types
import requests

# === YOUR API KEYS (already added) ===
TELEGRAM_TOKEN = "8032108432:AAEXz1oXL_dDHVjAu1FMFdBuzxi-8P4HNIA"
OPENROUTER_KEY = "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"

bot = TeleBot(TELEGRAM_TOKEN)
app = FastAPI()

@app.post("/")
async def process_webhook(request: Request):
    body = await request.json()
    update = types.Update.de_json(body)
    bot.process_new_updates([update])
    return {"ok": True}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://gabriel.vercel.app",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}],
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        bot.reply_to(message, reply.strip())
    except:
        bot.reply_to(message, "⚠️ Error getting AI reply.")
