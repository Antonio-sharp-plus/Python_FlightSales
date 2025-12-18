from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()


class NotificationManager:
    def __init__(self):
        self.RECEIVING_PHONE = os.getenv("TELEFONO")
        self.TWILIO_URL_ENCODE = os.getenv("URL_ENCODE_TWILIO")
        self.TOKEN_TWILIO = os.getenv("TOKEN_TWILIO")
        self.USER_TWILIO = os.getenv("USER_TWILIO")
        self.url = "https://api.twilio.com/2010-04-01/Accounts/ACc5e98f930560ce32c30a22bab371de67/Messages.json"

    def send_message(self, message):
        data = {
            "To": self.RECEIVING_PHONE,
            "MessagingServiceSid": self.TWILIO_URL_ENCODE,
            "Body": message
        }
        response = requests.post(
            self.url,
            data=data,
            auth=HTTPBasicAuth(self.USER_TWILIO, self.TOKEN_TWILIO)
        )
        response.raise_for_status()

        print(response.json())

# noti = NotificationManager()
# noti.send_message("tuni")
# the current code works
