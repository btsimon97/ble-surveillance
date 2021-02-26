import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# SMS CONSTANTS
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_TOKEN")
FROM_NUMBER = os.environ.get("TWILIO_PHONE")

#this function sends the final sms
def send_sms_message(recipient, msg):

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    return client.messages.create(
        body=msg,
        from_=FROM_NUMBER,
        to=recipient
    )


# this function creates an SMS text for warning the user about detected bluetooth devices
def send_detected_sms(recipient, bluetooth_device):
    msg = "We detected these unregistered bluetooth devices near your detector: "
    for device in bluetooth_device:
        if device == 0:
            msg = msg + device
        else:
            msg = msg + ", " + device
    return send_sms_message(recipient, msg)


def send_sms(sms_type, channel_data, bluetooth_devices = None):
    if(sms_type == "detection"):
        send_detected_sms(channel_data.recipient,bluetooth_devices)