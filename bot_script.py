
import telebot
import requests
# Your Telegram bot token
TELEGRAM_API_KEY = '8032108432:AAFivhR-duE5dpdhE8zkQTrP9Jy84cgGrnQ'

# Your OpenRouter API key
OPENROUTER_API_KEY = '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'

# Telegram Bot Setup
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Function to call OpenRouter AI
def get_ai_response(user_input):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai",  # Required
        "X-Title": "TelegramBot",  # Required
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Something went wrong. Try again later."

# Message Handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    response = get_ai_response(user_input)
    bot.reply_to(message, response)

print("Bot is running...")
bot.polling()
