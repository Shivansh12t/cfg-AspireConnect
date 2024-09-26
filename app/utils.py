from twilio.rest import Client
from config import TWILIO_WHATSAPP_NUMBER, ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp(to_number, message):
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f'whatsapp:{to_number}'
    )
