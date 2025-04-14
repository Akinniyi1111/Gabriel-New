import telebot
import requests

API_KEY = "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"
BOT_TOKEN = "8032108432:AAFivhR-duE5dpdhE8zkQTrP9Jy84cgGrnQ"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        prompt = message.text

        headers = {
            "Authorization": "Bearer " + API_KEY,  # Improved header concatenation
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openchat/openchat-3.5-1210",  # or another OpenRouter-supported model
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        
        # Print status code and response for debugging
        print(response.status_code)  # This will help us understand the response from the server
        data = response.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = "OpenRouter error: " + str(data)

        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")
        print(e)

bot.polling()
