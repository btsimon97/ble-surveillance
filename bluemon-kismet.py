#!/usr/bin/python3

import asyncio
import json
import websockets
import pathlib
import ssl
import configparser
import argparse
import logging

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
parser.add_argument("-ll", "--log-level", type=str,
                    help="Specify the logging level for the program. Defaults to INFO level. "
                         "Valid options are DEBUG, INFO, WARNING, ERROR, and CRITICAL",
                    default="INFO", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
parser.add_argument("-lf", "--log-file", type=str,
                   help="Specify the logging file to use. Default is /var/log/bluemon/bluemon-kismet.log",
                    default="/var/log/bluemon/bluemon-kismet.log")
parser.add_argument("-ukd","--unknown-kismet-device-file", type=str,
                    help="Specify the file with the list of unknown devices to diplay in GUI. Default is /etc/bluemon/unknown.conf",
                    default="/etc/bluemon/unknown_kismet.conf")
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

unknown_devices = configparser.ConfigParser()

# Setup logging
logging.basicConfig(filename=args.log_file, level=args.log_level, format='%(asctime)s %(levelname)s:%(message)s')


# Send alert based on zone settings
async def send_alert(zone, msg):
    notification_channels = [channel.lower().strip() for channel in
                             zones.get(zone, 'notification_channels').replace(']', '').replace('[', '').replace('"', '').split(",")]

    # Format message into notification server JSON
    message = {
        'message_type': 'detection',
        'zone_name': zone,
        'channel': notification_channels,
        'devices': msg
    }

    for channel in notification_channels:
        if channel == "email":
            recipients = [recipient.strip() for recipient in
                          zones.get(zone, 'email_recipients').replace(']', '').replace('[', '').replace('"', '').split(",")]
            message['email_data'] = {
                'recipients': recipients
            }
        elif channel == "sms":
            recipients = [recipient.strip() for recipient in
                          zones.get(zone, 'sms_recipients').replace(']', '').replace('[', '').replace('"', '').split(",")]
            message['sms_data'] = {
                'recipients': recipients
            }
        elif channel == "signal":
            recipients = [recipient.strip() for recipient in
                          zones.get(zone, 'sms_recipients').replace(']', '').replace('[', '').replace('"', '').split(",")]
            message['signal_data'] = {
                'recipients': recipients
            }
    # Connect to notification server socket and send message
    reader, writer = await asyncio.open_connection(config.get('notifications', 'server_name'),
                                                   config.getint('notifications', 'server_port'))
    writer.write(json.dumps(message).encode())
    writer.close()

async def write_to_unknown(name,mac):
    #reads in the current unknown config file
    unknown_devices.read(args.unknown_kismet__device_file)
    #adds a new section for the detected unknown device
    unknown_devices[name + "." + mac] = {'device_name': name, 'device_macaddr': mac}
    #removes some sections to ensure that the list is up to date (removes oldest first)
    while(len(unknown_devices.sections())>50):
        sectionRemove = unknown_devices.popitem()[0]
        unknown_devices.remove_section(sectionRemove)
    #writes back modified config file
    with open(args.unknown_kismet_device_file,'w') as configfile:
         unknown_devices.write(configfile)

# Process Received Message
async def process_message(message_json):
    zone = 'DEFAULT'
    device_mac = message_json['NEW_DEVICE']['kismet.device.base.macaddr']
    detected_by_uuid = message_json['NEW_DEVICE']['kismet.device.base.seenby'][0]['kismet.common.seenby.uuid']
    device_name = message_json['NEW_DEVICE']['kismet.device.base.commonname']
    # Determine if device is known or not
    device_known = False
    device_nickname = None
    for section in devices.sections():
        if devices.get(section, 'device_macaddr').upper() == device_mac.upper():
            device_known = True
            device_nickname = devices.get(section, 'device_nickname')
            break
    # Determine which zone has detected the device from the configured zones
    for section in zones.sections():
        if section != 'DEFAULT':
            if detected_by_uuid.upper() == zones.get(section, 'zone_uuid').upper():
                zone = section
                break
    # if device is unknown, add it to the unknown config file
    if not device_known and (device_name != device_mac):
        await write_to_unknown(device_name, device_mac)
    elif not device_known:
        await write_to_unknown("unknown", device_mac)
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
        elif zones.getboolean(zone, 'alert_on_recognized') and device_known:
            alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected known BTLE device " + device_nickname \
                            + " (" + device_mac + ")"

        # Build the log message for writing to the logs.
        log_message = "DEVICE DETECTION: Zone Name: " + zones.get(zone, 'zone_name') + " Zone UUID: " \
                      + zones.get(zone, 'zone_uuid') \
                      + " Known Device: " + str(device_known) \
                      + " Device Type: BTLE " \
                      + " Device MAC: " + device_mac

        # If the device name isn't the device's mac, indicating we know what its advertised name is.
        if device_name != device_mac:
            log_message += " Device Advertised Name: " + device_name

        # If the device had a user assigned nickname, append it to the log message.
        if device_nickname:
            log_message += " Device Nickname: " + device_nickname

        # Log the device event, regardless of alert settings.
        logging.info(log_message)

        # If alert message is defined, indicating we need to send an alert.
        if alert_message:
            await send_alert(zone, alert_message)



    elif message_json['NEW_DEVICE']['kismet.device.base.type'] == "BR/EDR" and zones.getboolean(zone, 'monitor_bt_devices'):
        if zones.getboolean(zone, 'alert_on_unrecognized') and not device_known:
            if device_name == device_mac:
                alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected an unknown BT device with MAC: " \
                                + device_mac
            else:
                alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected an unknown BT device with Name: " \
                                + device_name + " and MAC: " + device_mac
        elif zones.getboolean(zone, 'alert_on_recognized') and device_known:
            alert_message = "Zone " + zones.get(zone, 'zone_name') + " detected known BT device " + device_nickname \
                            + " (" + device_mac + ")"

        # Build the log message for writing to the logs.
        log_message = "DEVICE DETECTION: Zone Name: " + zones.get(zone, 'zone_name') + " Zone UUID: " \
                      + zones.get(zone, 'zone_uuid') \
                      + " Known Device: " + str(device_known) \
                      + " Device Type: BT " \
                      + " Device MAC: " + device_mac

        # If the device name isn't the device's mac, indicating we know what its advertised name is.
        if device_name != device_mac:
            log_message += " Device Advertised Name: " + device_name

        # If the device had a user assigned nickname, append it to the log message.
        if device_nickname:
            log_message += " Device Nickname: " + device_nickname

        # Log the device event, regardless of alert settings.
        logging.info(log_message)

        # If alert message is defined, indicating we need to send an alert.
        if alert_message:
            await send_alert(zone, alert_message)

    else:
        # Don't fire notification, but log something saying we got something to ignore.
        logging.debug("Ignoring Device event due to zone settings.")


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
                    logging.debug("Successfully connected to Kismet WebSocket.")
                    await websocket.send(subscription_message)  # send the subscribe message to kismet.
                    # Loop forever until the connection is closed.
                    while True:
                        try:
                            kismet_message = await websocket.recv()
                            await process_message(json.loads(kismet_message))
                            logging.debug(kismet_message)  # dump received message to log. Useful when debugging issues.
                        except websockets.exceptions.ConnectionClosed:
                            logging.debug("Connection to Kismet WebSocket was closed by Kismet. Will attempt to reconnect.")
                            break
            except OSError:
                logging.debug("Unable to connect to Kismet WebSocket. Maybe Kismet's not running?")
                await asyncio.sleep(1)

    else:
        uri = "ws://" + configuration['kismet']['server_name'] + ":" \
                       + configuration['kismet']['server_port'] + "/eventbus/events.ws?" \
                       + "KISMET=" + configuration['kismet']['api_token']
        # The actual websocket handling routine
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    logging.debug("Successfully connected to Kismet WebSocket.")
                    await websocket.send(subscription_message)  # send the subscribe message to kismet.
                    # Loop forever until the connection is closed.
                    while True:
                        try:
                            kismet_message = await websocket.recv()
                            await process_message(json.loads(kismet_message))
                            logging.debug(kismet_message)  # dump received message to log. Useful when debugging issues.
                        except websockets.exceptions.ConnectionClosed:
                            logging.debug("Connection to Kismet WebSocket was closed by Kismet. Will attempt to reconnect.")
                            break
            except OSError:
                logging.debug("Unable to connect to Kismet WebSocket. Maybe Kismet's not running?")
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
    kismet_websocket_task.cancel()
    event_loop.stop()
    event_loop.run_until_complete(event_loop.shutdown_asyncgens())
    event_loop.close()
# End Main Script Invocation
