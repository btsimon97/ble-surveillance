#!/usr/bin/python3

import os
import asyncio
import json
import websockets
import pathlib
import ssl
import configparser
import argparse

HOST = '127.0.0.1'        # Localhost
NOTIFICATION_PORT = 5555  # Notification server port

# Instantiate the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config-file", type=str,
                    help="Specify the bluemon config file to use. Default is /etc/bluemon/bluemon.conf",
                    default="/etc/bluemon/bluemon.conf")
parser.add_argument("-d", "--device-file", type=str,
                    help="Specify the file with the list of known devices to use. Default is /etc/bluemon/devices.conf",
                    default="/etc/bluemon/devices.conf")
parser.add_argument("-z", "--zone-file", type=str,
                    help="Specify the file with the list of zones to use. Default is /etc/bluemon/zones.conf",
                    default="/etc/bluemon/zones.conf")
args = parser.parse_args()

# Begin Script Functions Definition

# Read in the config file (this has to be at the top so other functions can read it).
config = configparser.ConfigParser()
config.read(args.config_file)

# Read in the zones config file
zones = configparser.ConfigParser(interpolation=None)
zones.read(args.zone_file)

# Read in the devices list
devices = configparser.ConfigParser(interpolation=None)
devices.read(args.device_file)


# device status(known or unknown) if messsage recieved from kismet
async def send_alert(zone, msg):
    notification_channels = zones.get(zone, 'notification_channels').replace(']', '').replace('[', '').replace('"', '').split(",")

    # Format message into notification server JSON
    message = {
        'message_type': 'detection',
        'zone_name': zone,
        'channel': notification_channels,
        'devices': msg
    }

    for channel in notification_channels:
        if channel == "email":
            message['email_data'] = {
                'recipients': zones.get(zone, 'email_recipients').replace(']', '').replace('[', '').replace('"', '').split(",")
            }
        elif channel == "sms":
            message['sms_data'] = {
                'recipients': zones.get(zone, 'sms_recipients').replace(']', '').replace('[', '').replace('"', '').split(",")
            }
        elif channel == "signal":
            message['signal_data'] = {
                'recipients': zones.get(zone, 'sms_recipients').replace(']', '').replace('[', '').replace('"', '').split(",")
            }
    # Connect to notification server socket and send message
    reader, writer = await asyncio.open_connection(config.get('notifications', 'server_name'),
                                                   config.getint('notifications', 'server_port'))
    writer.write(json.dumps(message).encode())
    writer.close()


# Process Received Message
async def process_message(message_json):
    zone = 'DEFAULT'
    device_mac = message_json['NEW_DEVICE']['kismet.device.base.macaddr']
    detected_by_uuid = message_json['NEW_DEVICE']['kismet.device.base.seenby'][0]['kismet.common.seenby.uuid']
    device_name = message_json['NEW_DEVICE']['kismet.device.base.commonname']
    # Determine if device is known or not
    device_known = False
    device_nickname = "Unknown Device"
    for section in devices.sections():
        if devices.get(section, 'device_macaddr') == device_name:
            device_known = True
            device_nickname = devices.get(section, 'device_nickname')
    # Determine which zone has detected the device from the configured zones
    for section in zones.sections():
        if section != 'DEFAULT':
            if detected_by_uuid == zones.get(section, 'zone_uuid'):
                zone = section
                break
    # Determine if notification settings for zone require notification and fire one if they do.
    alert_message = None
    if (message_json['NEW_DEVICE']['kismet.device.base.type'] == "BTLE" or message_json['NEW_DEVICE']['kismet.device.base.type'] == "BTLE Device") and zones.getboolean(zone, 'monitor_btle_devices'):
        if zones.getboolean(zone, 'alert_on_unrecognized') and not device_known:
            # Fire Notification
            if device_name == device_mac:
                alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected an unknown BTLE device with MAC: " \
                                + device_mac
            else:
                alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected an unknown BTLE device with Name: " \
                                + device_name + " and MAC: " + device_mac
        elif zones.getboolean(zone, 'alert_on_recognized'):
            alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected known BTLE device " + device_nickname \
                            + " (" + device_mac + ")"

        if alert_message:
            print(alert_message, flush=True)
            await send_alert(zone, alert_message)

    elif message_json['NEW_DEVICE']['kismet.device.base.type'] == "BR/EDR" and zones.getboolean(zone, 'monitor_bt_devices'):
        if zones.getboolean(zone, 'alert_on_unrecognized') and not device_known:
            if device_name == device_mac:
                alert_message = "Zone " + zones.get(zone, 'zone_name') + "detected an unknown BT device with MAC: " \
                                + device_mac
            else:
                alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected an unknown BT device with Name: " \
                                + device_name + " and MAC: " + device_mac
        elif zones.getboolean(zone, 'alert_on_recognized'):
            alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected known BT device " + device_nickname \
                            + " (" + device_mac + ")"

        if alert_message:
            print(alert_message, flush=True)
            await send_alert(zone, alert_message)
    else:
        # Don't fire notification, but print something saying we got something to ignore.
        print("Ignoring Device event due to notification settings.", flush=True)


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
                            await process_message(json.loads(kismet_message))
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
                            await process_message(json.loads(kismet_message))
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
    kismet_websocket_task = asyncio.ensure_future(kismet_websocket(config))  # Add websocket coroutine for Kismet
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
