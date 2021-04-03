import socket
import asyncio
import concurrent.futures
import json

import emailer
import sms

HOST = '127.0.0.1'  # Localhost
PORT = 5555        # Port to listen on


async def handle_connection(reader, writer):
    while True:
        message = await reader.read()
        if not message:  # Quit loop once data stops being received for connection.
            break
        message = json.loads(message.decode())
        event_loop = asyncio.get_running_loop()  # get event loop for running sync code in executor to avoid deadlock

        if "email" in message['channel']:
            # Run the email function in a different thread to avoid bogging down the main thread.
            with concurrent.futures.ThreadPoolExecutor() as email_pool:
                await event_loop.run_in_executor(email_pool, emailer.send_email,
                                                 message['message_type'], message['email_data'], message['devices'])

        if "sms" in message['channel']:
            # Run the SMS function in a different thread to avoid tying up main thread.
            with concurrent.futures.ThreadPoolExecutor() as sms_pool:
                await event_loop.run_in_executor(sms_pool, sms.send_sms,
                                                 message['message_type'], message['sms_data'], message['devices'])

    writer.close()  # close the writer since connection is done now.


async def main():
    server = await asyncio.start_server(handle_connection, HOST, PORT)
    async with server:
        await server.serve_forever()

#if __name__ == "__main__":
#
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#        s.bind((HOST, PORT))
#        s.listen()
#        while True:
#            conn, addr = s.accept()
#            with conn:
#                while True:
#                    data = conn.recv(1024)
#                    if not data:
#                        break
#                    msg_data = json.loads(data.decode())
#                    print(msg_data)
#                    # if "email" in msg_data.channel:
#                    #     emailer.send_email(msg_data.message_type, msg_data.email_data, msg_data.devices)
#                    # if "sms" in msg_data.channel:
#                    #     sms.send_sms(msg_data.message_type, msg_data.sms_data, msg_data.devices)

