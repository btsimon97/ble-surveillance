import socket
import asyncio
import concurrent.futures
import json
import configparser
import argparse
import emailer
import sms

# Instantiate the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--bind-address", type=str,
                    help="IP address to bind to for connections. Default is 0.0.0.0, or bind to all interfaces",
                    default="0.0.0.0")

parser.add_argument("-c", "--config-file", type=str,
                    help="Specify the notifications config file to use. Default is /etc/bluemon/notifications.conf",
                    default="/etc/bluemon/notifications.conf")

parser.add_argument("-p", "--bind-port", type=int,
                    help="TCP port number to bind to for connections. Default is 5555.", 
                    default=5555)
args = parser.parse_args()

# Read in the config file (this has to be at the top so other functions can read it).
config = configparser.ConfigParser()
config.read(args.config_file)


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
                await event_loop.run_in_executor(email_pool, emailer.send_email, config,
                                                 message['message_type'], message['email_data'], message['devices'])

        if "sms" in message['channel']:
            # Run the SMS function in a different thread to avoid tying up main thread.
            with concurrent.futures.ThreadPoolExecutor() as sms_pool:
                await event_loop.run_in_executor(sms_pool, sms.send_sms, config,
                                                 message['message_type'], message['sms_data'], message['devices'])

    writer.close()  # close the writer since connection is done now.


async def main():
    server = await asyncio.start_server(handle_connection, args.bind_address, args.bind_port)
    async with server:
        await server.serve_forever()


asyncio.run(main())
