import requests
from config import BOT_TOKEN, CHANNEL_ID


def send_signal(message, image):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(image,"rb") as photo:

        requests.post(
            url,
            data={"chat_id": CHANNEL_ID, "caption": message},
            files={"photo": photo}
        )
