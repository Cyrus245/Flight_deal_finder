from twilio.rest import Client
from dotenv import dotenv_values

config = {
    **dotenv_values('.env')
}

s_id = config['twilio_sid']
auth_token = config['twilio_token']
sender_no = config['twilio_number']
receiver_no = config['receiver_number']


class NotificationManager:
    def __init__(self):
        self.client = Client(s_id, auth_token)

    def seng_msg(self, message):
        self.client.messages.create(body=message, from_=sender_no, to=receiver_no)
