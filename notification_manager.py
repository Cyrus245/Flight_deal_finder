from twilio.rest import Client
from dotenv import dotenv_values
import smtplib

config = {
    **dotenv_values('.env')
}

s_id = config['twilio_sid']
auth_token = config['twilio_token']
sender_no = config['twilio_number']
receiver_no = config['receiver_number']
my_email = config['my_email']
my_pass = config['my_pass']


class NotificationManager:
    def __init__(self):
        self.client = Client(s_id, auth_token)

    def seng_msg(self, message):
        """This method will send sms"""
        self.client.messages.create(body=message, from_=sender_no, to=receiver_no)

    def send_emails(self, emails, message, link):
        """This method will send email"""
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_pass)
            print('login success')

            for email in emails:
                # sending email
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{link}".encode('utf-8'))
                print("mail sent")
