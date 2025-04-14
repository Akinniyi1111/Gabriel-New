import telebot
import requests

# Your actual Telegram bot token
BOT_TOKEN = "8032108432:AAFivhR-duE5dpdhE8zkQTrP9Jy84cgGrnQ"

# Your OpenRouter API Key
ROUTER_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Ask me anything.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    headers = {
        "Authorization": f"Bearer {ROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openchat/openchat-3.5",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = f"❌ Error {response.status_code}: {response.text}"

    except Exception as e:
        reply = f"⚠️ An error occurred: {str(e)}"

    bot.reply_to(message, reply)

bot.polling()
