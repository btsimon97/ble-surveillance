#!/usr/bin/python3

import os
import asyncio
import json
import socket
import configparser
import argparse
import re


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

# Begin Script Constants Definition
message_socket_path = '/run/bluemon/eventdata.socket'  # Path and name of the listening socket.
message_socket_permissions = 0o660  # Socket Permissions, see note in setup function for more info.
message_max_size = 1024  # Max size of single message in bytes. Anything longer is truncated. Must be power of 2
# End Script Constants Definition


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

# Get environment variables from systemd that we use to connect to the socket.
LISTEN_FDS = int(os.environ.get("LISTEN_FDS", 0))
LISTEN_PID = os.environ.get("LISTEN_PID", None) or os.getpid()


# sends the appropriate message based on zone settings
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
    detected_by_uuid = message_json['ubertooth_serial_number']
    for section in zones.sections():
        if section != 'DEFAULT':
            if detected_by_uuid == zones.get(section, 'zone_uuid'):
                zone = section
    if zones.getboolean(zone, 'monitor_bt_devices'):
        #  Compile a regex to identify results with an unknown UAP
        unknown_uap_regex = re.compile('(\?{2}\:){3}(([a-f]|[A-F]|[0-9]){2}\:?){3}')
        #  Compile regex to extract LAP of device from reported MAC
        lap_regex = re.compile('(([a-f]|[A-F]|[0-9]){2}\:?){3}')
        #  Compile regex to extract UAP and LAP of device from reported MAC
        uap_and_lap_regex = re.compile('(([a-f]|[A-F]|[0-9]){2}\:?){4}')
        for device in message_json['scan_results']:
            device_known = False
            device_nickname = ""
            device_advertised_name = ""  # what the device advertises its name as in discovery packets, not always known
            device_mac = device['mac']
            if 'name' in device:
                device_advertised_name = device['name']
                
            #  if device's UAP isn't known and the zone isn't configured to ignore unknown UAP devices
            if unknown_uap_regex.match(device['mac']) and not zones.getboolean(zone, 'ignore_devices_with_unknown_uap'):
                lap = lap_regex.search(device['mac'])[0]  # extract LAP from device mac string
                for section in devices.sections():  # see if the device's LAP matches a known LAP
                    current_mac = devices.get(section, 'device_macaddr')
                    if lap in current_mac:
                        device_known = True
                        device_nickname = devices.get(section, 'device_nickname')
                        device_mac = current_mac
                        break

            #  device's UAP is known
            else:
                uap_and_lap = uap_and_lap_regex.search(device['mac'])[0]
                for section in devices.sections():  # see if UAP and LAP matches known UAP and LAP
                    current_mac = devices.get(section, 'device_macaddr')
                    if uap_and_lap in current_mac:
                        device_known = True
                        device_nickname = devices.get(section, 'device_nickname')
                        device_mac = current_mac
                        break
            
            if device_known:
                alert_message = "Detected known device " + device_nickname + " (" + device_mac + ")"
            
            elif device_advertised_name and (device_advertised_name != device_mac):
                alert_message = "Detected an unknown device with Name: " + device_advertised_name + " and MAC: " + device_mac
                
            else:
                alert_message = "Detected an unknown device with MAC: " + device_mac
                
            print(alert_message, flush=True)
            await send_alert(zone, alert_message)
    
    else:
        # Ignore device event since zone doesn't care about BT devices
        print("Ignoring device event due to zone settings.", flush=True)


# Handle incoming connections and process received messages.
async def handle_connection(reader, writer):
    while True:
        message = await reader.read(message_max_size)  # Wait until data is available
        if not message:  # Quit the loop when we stop getting data
            break
        message = message.decode()
        await process_message(json.loads(message))
        print(message, flush=True)  # Replace this with a function call to dispatch messages to the notification server.
    writer.close()


# Socket loop, handles incoming UNIX socket connections (TODO: Implement signal handling so socket is properly cleaned up)
async def unix_socket():
    # Detect if we're running through systemd or not
    if LISTEN_FDS == 0:  # Not running via systemd or systemd didn't pass the FDs we need
        # Detect if socket file already exists and clean it up if it does
        if os.path.exists(message_socket_path):
            os.unlink(message_socket_path)
        server = await asyncio.start_unix_server(handle_connection, path=message_socket_path, start_serving=False)
        os.chmod(message_socket_path, message_socket_permissions)
    else:  # We're running in systemd, use the FD that systemd gives us to setup the socket.
        fd_socket = socket.fromfd(3, socket.AF_UNIX, socket.SOCK_STREAM)
        server = await asyncio.start_unix_server(handle_connection, sock=fd_socket, start_serving=False)
    async with server:
        await server.serve_forever()

# End Script Functions Definition


# Begin Main Script Invocation
event_loop = asyncio.get_event_loop()
try:
    unix_socket_task = asyncio.ensure_future(unix_socket())  # Add the UNIX socket coroutine to handle incoming data
    event_loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Shutting Down...")
    unix_socket_task.cancel()
    event_loop.stop()
    event_loop.run_until_complete(event_loop.shutdown_asyncgens())
    event_loop.close()
# End Main Script Invocation
