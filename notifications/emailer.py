import smtplib, ssl, os

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

#EMAILER CONSTANTS
PORT = 465
PASSWORD = os.environ.get('EMAIL_PASSWORD')
USERNAME = os.environ.get('EMAIL_USERNAME')

# MESSAGES
#===========
# For now these will be stored here, although they can be extracted to another file and imported
# if this becomes too cluttered. The formate for message values is CONTENT_{TYPE}_{FORMAT}
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

#This function creates the message object and formats the devices onto the content
def create_detected_message(bluetooth_devices):
    msg = MIMEMultipart("alternative")

    device_string_text = ""
    device_string_html = ""

    #create devices string for plaintext
    for device in bluetooth_devices:
        device_string_text = device_string_text + device + "\n"

    #create devices string for html
    for device in bluetooth_devices:
        device_string_html = device_string_text + "<li>" + device + "</li>"

    #embed device strings into content and attach to message object, html will be tried first
    msg.attach(MIMEText(CONTENT_DETECTED_TEXT.format(text_bluetooth_elements=device_string_text), "plain"))
    msg.attach(MIMEText(CONTENT_DETECTED_HTML.format(text_bluetooth_elements=device_string_html), "html"))

    msg['Subject'] = "Unregistered bluetooth devices detected"

    return msg

#This function sends the final email, will be used for all types
def send(recipient, msg, server):
    server.login(USERNAME, PASSWORD)

    server.sendmail(USERNAME, recipient, msg.as_string())
    server.quit()

    return 1

#This function creates an email for warning the user about detected bluetooth devices
def send_detected_email(recipient, bluetooth_devices):
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:

        msg = create_detected_message(bluetooth_devices)
        return send(recipient, msg, server)