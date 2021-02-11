import socket
import json
import time

HOST = '127.0.0.1'  # Localhost
PORT = 5555        # The port used by the server

bluetooth_data = [
    {
        'channel': ['email'],
        'type': 'detection',
        'devices': ['car', 'house']
    },
    {
        'channel': ['sms'],
        'type': 'detection',
        'devices': ['dog', 'secret camera']
    },
    {
        'channel': ['email', 'sms'],
        'type': 'detection',
        'devices': []
    }
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    send_data = json.dumps(bluetooth_data[0])
    s.connect((HOST, PORT))
    s.sendall(str.encode(send_data))
    time.sleep(2)
    send_data = json.dumps(bluetooth_data[1])
    s.sendall(str.encode(send_data))
    time.sleep(10)
    send_data = json.dumps(bluetooth_data[2])
    s.sendall(str.encode(send_data))
