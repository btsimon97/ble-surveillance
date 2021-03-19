#!/usr/bin/python3

import os
import asyncio
import json
import websockets
import pathlib
import ssl
import configparser


# Begin Script Functions Definition

# Read in the config file (this has to be at the top so other functions can read it).
config = configparser.ConfigParser()
config.read('/etc/bluemon/bluemon.conf')  # TODO: Implement argparse so filename is set by CLI arg instead of hardcoded

# Read in the zones config file
zones = configparser.ConfigParser(interpolation=None)
zones.read('/etc/bluemon/zones.conf')

# Read in the devices list
devices = configparser.ConfigParser(interpolation=None)
devices.read('/etc/bluemon/devices.conf')


# device status(known or unknown) if messsage recieved from kismet
def device_status_k(device_name):
    device_known = False
    device_nickname = "Unknown Device"
    for section in devices.sections():
        if devices.get(section, 'device_macaddr') == device_name:
            device_known = True
            device_nickname = devices.get(section, 'device_nickname')
    return device_known, device_nickname


# determine whether the message requires notificaiton
def message_eligibility(dev_type, zone, device_known, nickname, macaddr, ubertoothName):
    eligibility = False
    monitor_unknown = not device_known & (zones.get(zone, 'alert_on_unrecognized') == 'true')
    monitor_known = device_known & (zones.get(zone, 'alert_on_recognized') == 'true')
    monitor = False
    if dev_type == 'BTLE' or dev_type == 'BTLE Device':
        if zones.get(zone, 'monitor_btle_devices') == 'true':
            monitor = True
    else:
        if zones.get(zone, 'monitor_bt_devices') == 'true':
            monitor = True
    if (monitor_known | monitor_unknown) & monitor:
        msg = nickname + " (" + ubertoothName + macaddr + ") " + " detected"
        eligibility = True
    else:
        msg = "Ignoring Device event due to zone config settings."

    return eligibility, msg


# sends the appropriate message based on zone settings
def send_message(zone, msg):
    notification_channels = zones.get(zone, 'notification_channels').replace(']', '').replace('[', '').replace('"', '').split(",")
    for channel in notification_channels:
        if channel == "email":
            print("Sent Email, " + msg)  # placeholders  until we set up messaging service
        elif channel == "sms":
            print("Sent SMS,  " + msg)
        elif channel == "signal":
            print("Sent SMS,  " + msg)
            # Format message into notification server JSON
            # Connect to notification server socket
            # Send notification message.


# Process Received Message
def process_message(message):
    message_json = json.loads(message)
    zone = 'DEFAULT'
    notify = False
    message_json = message['NEW_DEVICE']
    device_mac = message_json['kismet.device.base.macaddr']
    detected_by_uuid = message_json['kismet.device.base.seenby'][0]['kismet.common.seenby.uuid']
    device_known, nickname = device_status_k(device_mac)
    # Determine which zone has detected the device from the configured zones
    for section in zones.sections():
        if section != 'DEFAULT':
            if detected_by_uuid == zones.get(section, 'zone_uuid'):
                zone = section
    # Determine the notification settings for that zone
    dev_type = message_json['kismet.device.base.type']
    sendMsg, msg = message_eligibility(dev_type, zone, device_known, nickname, device_mac, "")
    if(sendMsg):
        send_message(zone, msg)


async def kismet_websocket(configuration):
    uri = ""
    ssl_context = None  # Used for TLS websocket sessions, initialized here so it can be setup later.

    # message sent to kismet to get device data, along with some field simplification to reduce the data we get back.
    # split across multiple lines for better visibility.
    subscription_message = '{"SUBSCRIBE": "NEW_DEVICE", "fields":["kismet.device.base.seenby","kismet.device.base.macaddr","kismet.device.base.commonname","kismet.device.base.type"]}'

    # build the kismet websocket URI using the configuration file data
    if configuration['kismet'].getboolean('use_tls'):
        uri = "wss://" + configuration['kismet']['server_name'] + ":" \
                       + configuration['kismet']['server_port'] + "/eventbus/events.ws?" \
                       + "KISMET=" + configuration['kismet']['api_token']
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
                            process_message(kismet_message)
                            print(kismet_message, flush=True)  # Remove this when we get a production ready version
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
                       + "KISMET=" + configuration['kismet']['api_token']
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
                            process_message(kismet_message)
                            print(kismet_message, flush=True)  # Remove this when we get a production ready version.
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
    kismet_websocket_task = asyncio.ensure_future(kismet_websocket(config))  # Add websocket coroutine to get Kismet data
    event_loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Shutting Down...")
    kismet_websocket_task.cancel()
    event_loop.stop()
    event_loop.run_until_complete(event_loop.shutdown_asyncgens())
    event_loop.close()
# End Main Script Invocation
