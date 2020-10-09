import emailer

def send_email(email_type, recipient, bluetooth_devices=None):

    if(email_type == "detection"):
        emailer.send_detected_email(recipient, bluetooth_devices)
    # Added an email_type so that different types of emails can potentially be sent
    #(ie. welcome, devices changed, etc.)

#other functions for sending other type of notifications, then main file will only have to import this
