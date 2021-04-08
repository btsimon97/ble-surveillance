import os
import configparser

from twilio.rest import Client


# this function sends the final sms
def send_sms_message(sms_config, recipient, msg):
    account_sid = sms_config.get('sms', 'twilio_account_sid')
    auth_token = sms_config.get('sms', 'twilio_auth_token')
    sender = sms_config.get('sms', 'sender_phone_number')
    client = Client(account_sid, auth_token)
    return client.messages.create(
        body=msg,
        from_=sender,
        to=recipient
    )


# External function called by main notification server code.
def send_sms(sms_config, sms_type, channel_data, bluetooth_devices=None):
    if sms_type == "detection":
        for recipient in channel_data['recipients']:
            send_sms_message(sms_config, recipient, bluetooth_devices)