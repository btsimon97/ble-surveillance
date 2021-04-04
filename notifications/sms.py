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


# this function creates an SMS text for warning the user about detected bluetooth devices
def send_detected_sms(sms_config, recipient, bluetooth_device):
    msg = "We detected these unregistered bluetooth devices near your detector: "
    for device in bluetooth_device:
        if device == 0:
            msg = msg + device
        else:
            msg = msg + ", " + device
    return send_sms_message(recipient, msg)


# External function called by main notification server code.
def send_sms(sms_config, sms_type, channel_data, bluetooth_devices=None):
    if sms_type == "detection":
        send_detected_sms(sms_config, channel_data.recipient, bluetooth_devices)
