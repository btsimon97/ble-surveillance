import socket
import json

import emailer
import sms

HOST = '127.0.0.1'  # Localhost
PORT = 5555        # Port to listen on

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
                        emailer.send_email(msg_data.message_type, msg_data.channel_data, msg_data.devices)
                    if msg_data.channel == "sms":
                        sms.send_sms(msg_data.message_type, msg_data.channel_data, msg_data.devices)

