import smtplib
import ssl
import textwrap
import configparser

from email.message import EmailMessage
from email import policy


# Build the alert message for sending using SMTPlib
def build_alert_email(email_config, recipients, message_data):
    alert_email_message = EmailMessage(policy=policy.SMTP)  # set the message policy to use CRLF line endings.
    alert_email_message.set_content(textwrap.fill(message_data), width=78)  # Set message body
    alert_email_message['Subject'] = email_config.get('email', 'email_subject')  # set subject line according to config.
    alert_email_message['From'] = email_config.get('email', 'email_address')  # Set from address using config
    alert_email_message['To'] = recipients  # Set recipients from passed in value
    return alert_email_message  # return constructed message to caller


# External function called by notification server.
def send_email(email_config, email_type, channel_data, bluetooth_devices=None):
    message = None
    if email_type == "detection":
        # Construct message to be sent
        message = build_alert_email(email_config, channel_data['recipients'], bluetooth_devices)

    # Server connection is NOT encrypted at all.
    if email_config.get('email', 'smtp_connection_method') == "plain":
        with smtplib.SMTP(host=email_config.get('email', 'smtp_servername'),
                          port=email_config.getint('email', 'smtp_portnumber')) as server:
            
            # Authenticate to server if it requires authentication
            if email_config.getboolean('email', 'smtp_authentication_required'):
                server.login(user=email_config.get('email', 'smtp_username'), 
                             password=email_config.get('email', 'smtp_password'))
            server.send_message(message)  # Send constructed message
            server.quit()  # close the SMTP server connection.
    
    # Server connection starts unencrypted then upgrades to encrypted via STARTTLS command
    elif email_config.get('email', 'smtp_connection_method') == "STARTTLS":
        with smtplib.SMTP(host=email_config.get('email', 'smtp_servername'),
                          port=email_config.getint('email', 'smtp_portnumber')) as server:
            
            # Send STARTTLS to upgrade connection to encrypted
            server.starttls(context=ssl.create_default_context())
            # Authenticate to server if it requires authentication
            if email_config.getboolean('email', 'smtp_authentication_required'):
                server.login(user=email_config.get('email', 'smtp_username'), 
                             password=email_config.get('email', 'smtp_password'))
            server.send_message(message)  # Send constructed message
            server.quit()  # close the SMTP server connection.

    # For all other possible values, assume connection must already start encrypted with TLS
    else:
        with smtplib.SMTP_SSL(host=email_config.get('email', 'smtp_servername'),
                              port=email_config.getint('email', 'smtp_portnumber'),
                              context=ssl.create_default_context()) as server:
            
            # Authenticate to server if it requires authentication
            if email_config.getboolean('email', 'smtp_authentication_required'):
                server.login(user=email_config.get('email', 'smtp_username'),
                             password=email_config.get('email', 'smtp_password'))
            server.send_message(message)  # Send constructed message
            server.quit()  # close the SMTP server connection.
