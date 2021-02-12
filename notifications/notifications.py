import emailer
import socket
import json
import sms

HOST = '127.0.0.1'  # Localhost
PORT = 5555        # Port to listen on

def send_email(email_type, recipient, bluetooth_devices=None):

    if(email_type == "detection"):
        emailer.send_detected_email(recipient, bluetooth_devices)
    # Added an email_type so that different types of emails can potentially be sent
    #(ie. welcome, devices changed, etc.)

#other functions for sending other type of notifications, then main file will only have to import this

def send_sms(sms_type,recipient, bluetooth_devices = None):
    if(sms_type == "detection"):
        sms.send_detected_sms(recipient,bluetooth_devices)

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    msg_data = json.loads(data.decode())
                    if msg_data.channel == "email":
                        send_email(msg_data.message_type, msg_data.email, msg_data.devices)
                    if msg_data.channel == "sms":
                        send_sms(msg_data.message_type, msg_data.email, msg_data.devices)

