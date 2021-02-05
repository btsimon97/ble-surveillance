#!/usr/bin/python3

import os
import asyncio
import json
import websockets
import pathlib
import ssl
import configparser

# Begin Script Constants Definition
message_socket_path = '/run/bt-surveillance/processing.sock'  # Path and name of the listening socket.
message_socket = None  # Actual socket we'll be getting messages from. Initialized to None until socket is setup.
message_socket_permissions = 0o666  # Socket Permissions, see note in setup function for more info.
message_max_size = 1024  # Max size of single message in bytes. Anything longer is truncated. Must be power of 2
# End Script Constants Definition


# Begin Script Functions Definition

# Read in the config file (this has to be at the top so other functions can read it).
config = configparser.ConfigParser()
config.read('/etc/ble-surveillance.conf')  # TODO: Implement argparse so filename is set by CLI arg instead of hardcoded


# Identify what type of message was received (i.e. what program sent it)
def get_message_type(message):
    message_json = json.loads(message)
    if ("kismet.device.base.macaddr" in message_json) or ("kismet.device.base.commonname" in message_json):
        return "kismet"

    elif ("mac" in message_json) or ("name" in message_json):
        return "ubertooth"

    else:
        return "unknown"

def device_status(device_name):
    configParser = configparser.RawConfigParser()
    configFilePath = r'devices.conf.example'
    configParser.read(configFilePath)
    device_known = False
    for section in configParser.sections():
        if configParser.get(section,'device_name') == device_name:
            device_known = True
    return device_known

# Process Received Message
def process_message(message):
    message_json = json.loads(message)
    configParser = configparser.RawConfigParser()
    configFilePath = r'zones.conf'
    configParser.read(configFilePath)
    zone = ''
    if get_message_type(message) == "kismet":
        device_name = message_json['kismet.device.base.commonname']
        device_mac = message_json['kismet.device.base.macaddr']
        detected_by_uuid = message_json['kismet.device.base.seenby'][0]['kismet.common.seenby.uuid']
        device_known = device_status(device_name)
        # Determine which zone has detected the device from the configured zones
        for section in configParser.sections():
            if section != 'DEFAULT':
                if detected_by_uuid == configParser.get(section,'zone_uuid'):
                   zone = section
        # Determine the notification settings for that zone
        # need to set up code to check default if a certain section doesn't exist for zone
        # If notification settings for zone demand a notification be sent:
        notification_channels = configParser.get(zone, 'notification_channels').replace(']', '').replace('[', '').replace('"', '').split(",")
        for channel in notification_channels:
            if channel == "email":
                    print("Sent Email") # placeholders  until we set up messaging service
            elif channel == "sms":
                    print("Sent SMS")
            elif channel == "signal":
                    print("Sent SMS")
            # Format message into notification server JSON
            # Connect to notification server socket
            # Send notification message.

    elif get_message_type(message) == "ubertooth":
        print("Working...")
        # Determine if device is known or not
        # Grab the default Zone config settings since we don't attach a UUID to these messages
        # If notification settings demand notification be sent:
            # Format message into notification server JSON
            # Connect to notification server socket
            # Send notification message
    else:
        print("Received a message of unknown type, ignoring.")


# Handle incoming connections and process received messages.
async def handle_connection(reader, writer):
    while True:
        message = await reader.read(message_max_size)  # Wait until data is available
        if not message:  # Quit the loop when we stop getting data
            break
        message = message.decode()
        print(message, flush=True)  # Replace this with a function call to dispatch messages to the notification server.
    writer.close()


# Socket loop, handles incoming UNIX socket connections (TODO: Implement signal handling so socket is properly cleaned up)
async def unix_socket():
    # Detect if socket file already exists and clean it up if it does
#    if os.path.exists(message_socket_path):
#        os.unlink(message_socket_path)
#    server = await asyncio.start_unix_server(handle_connection, path=message_socket_path, start_serving=False)
#    os.chmod(message_socket_path, message_socket_permissions)
#    async with server:
#        await server.serve_forever()


# Connect to Kismet WebSocket for device data retrieval
async def kismet_websocket(configuration):
    uri = ""
    ssl_context = None # Used for TLS websocket sessions, initialized here so it can be setup later.

    # message sent to kismet to get device data, along with some field simplification to reduce the data we get back.
    # split across multiple lines for better visibility.
    subscription_message = '{"SUBSCRIBE": "NEW_DEVICE", "fields": ["kismet.device.base.macaddr","kismet.device.base.commonname","kismet.device.base.seenby"]}'

    # build the kismet websocket URI using the configuration file data
    if configuration['kismet'].getboolean('use_tls'):
        uri = "wss://" + configuration['kismet']['server_name'] + ":" \
                       + configuration['kismet']['server_port'] + "/eventbus/events.ws?" \
                       + "user=" + configuration['kismet']['username'] \
                       + "&password=" + configuration['kismet']['password']
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_ca_cert = pathlib.Path(__file__).with_name(configuration['kismet']['tls_cert_file'])
        ssl_context.load_verify_locations(ssl_ca_cert)

        while True:
            try:
                async with websockets.connect(uri, ssl=ssl_context) as websocket:
                    print("Successfully connected to Kismet WebSocket.", flush=True)
                    await websocket.send(subscription_message)  # send the subscribe message to kismet.
                    # Loop forever until the connection is closed.
                    while True:
                        try:
                            kismet_message = await websocket.recv()
                            print(kismet_message, flush=True)  # replace this with a function call to the processing function.
                        except websockets.exceptions.ConnectionClosed:
                            print("Connection to Kismet WebSocket was closed by Kismet. Will attempt to reconnect.")
                            break
            except OSError:
                print("Unable to connect to Kismet WebSocket. Maybe Kismet's not running?", flush=True)
                print("Retrying in 1 Second...", flush=True)
                await asyncio.sleep(1)

    else:
        uri = "ws://" + configuration['kismet']['server_name'] + ":" \
                       + configuration['kismet']['server_port'] + "/eventbus/events.ws?" \
                       + "user=" + configuration['kismet']['username'] \
                       + "&password=" + configuration['kismet']['password']
        # The actual websocket handling routine
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    print("Successfully connected to Kismet WebSocket.", flush=True)
                    await websocket.send(subscription_message)  # send the subscribe message to kismet.
                    # Loop forever until the connection is closed.
                    while True:
                        try:
                            kismet_message = await websocket.recv()
                            print(kismet_message)  # replace this with a function call to the processing function.
                        except websockets.exceptions.ConnectionClosed:
                            print("Connection to Kismet WebSocket was closed by Kismet. Will attempt to reconnect.")
                            break
            except OSError:
                print("Unable to connect to Kismet WebSocket. Maybe Kismet's not running?", flush=True)
                print("Retrying in 1 Second...", flush=True)
                await asyncio.sleep(1)
# End Script Functions Definition


# Begin Main Script Invocation
event_loop = asyncio.get_event_loop()
try:
    unix_socket_task = asyncio.ensure_future(unix_socket())  # Add the UNIX socket coroutine to handle incoming data
    kismet_websocket_task = asyncio.ensure_future(kismet_websocket(config))  # Add websocket coroutine to get Kismet data
    event_loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Shutting Down...")
    unix_socket_task.cancel()
    kismet_websocket_task.cancel()
    event_loop.stop()
    event_loop.run_until_complete(event_loop.shutdown_asyncgens())
    event_loop.close()
# End Main Script Invocation
