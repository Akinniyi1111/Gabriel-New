import requests

TOKEN = "8032108432:AAEXz1oXL_dDHVjAu1FMFdBuzxi-8P4HNIA"
URL = "https://gabriel.vercel.app"

r = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
print(r.text)
