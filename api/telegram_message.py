import requests

from . import conf
from io import BytesIO
import requests
# from PIL import Image

photo_url = f"https://api.telegram.org/{conf.bottoken}/sendPhoto"
message_url = f"https://api.telegram.org/{conf.bottoken}/sendMessage"

# with open('internship certificate.png','rb') as file:
#     data = file.read()




headers = {
    "accept": "application/json",
    "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
    "content-type": "image/png"
}

# image_response = requests.get("")
# image = 

# with BytesIO() as output:
#     image.save(output, format='PNG')
#     output.seek(0)

def send_message(message):
    payload = {
    "chat_id": "@weather845173",
    "text":message,
    "caption": "Optional",
    "disable_notification": False,
    "reply_to_message_id": None
    }
    response = requests.post(message_url, data=payload)

    print(response.content)

#     print(response.text)

# send_message("hello")