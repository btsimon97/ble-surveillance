import smtplib, ssl, os

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

PORT = 465
PASSWORD = os.environ.get('EMAIL_PASSWORD')
USERNAME = os.environ.get('EMAIL_USERNAME')

CONTENT_DETECTED_TEXT = """\
Unregistered bluetooth devices have been detected!

Hi, we detected these unregisted bluetooth devices near your detector:

{text_bluetooth_elements}
"""
CONTENT_DETECTED_HTML = """\
<html>
    <head>Unregistered bluetooth devices have been detected!</head>
    <body>
        <p>Hi, we detected these unregisted bluetooth devices near your detector:</p>
        <p>
            <ul>
                {html_bluetooth_elements}
            </ul>
        </p>
    </body>
</html>
"""

def create_detected_message(bluetooth_devices):
    msg = MIMEMultipart("alternative")

    device_string_text = ""
    device_string_html = ""

    for device in bluetooth_devices:
        device_string_text = device_string_text + device + "\n"

    for device in bluetooth_devices:
        device_string_html = device_string_text + "<li>" + device + "</li>"

    msg.attach(MIMEText(CONTENT_DETECTED_TEXT.format(text_bluetooth_elements=device_string_text), "plain"))
    msg.attach(MIMEText(CONTENT_DETECTED_HTML.format(text_bluetooth_elements=device_string_html), "html"))

    msg['Subject'] = "Unregistered bluetooth devices detected"

    return msg

def send(recipient, msg, server):
    server.login(USERNAME, PASSWORD)

    server.sendmail(USERNAME, recipient, msg.as_string())
    server.quit()

    return 1

def send_detected_email(recipient, bluetooth_devices):
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:

        msg = create_detected_message(bluetooth_devices)
        return send(recipient, msg, server)
