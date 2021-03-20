#!/usr/bin/python3

import os
import asyncio
import socket
import json
import configparser

# Begin Script Constants Definition
message_socket_path = '/run/bluemon/eventdata.socket'  # Path and name of the listening socket.
message_socket = None  # Actual socket we'll be getting messages from. Initialized to None until socket is setup.
message_socket_permissions = 0o660  # Socket Permissions, see note in setup function for more info.
message_max_size = 1024  # Max size of single message in bytes. Anything longer is truncated. Must be power of 2
# End Script Constants Definition


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

# Get environment variables from systemd that we use to connect to the socket.
LISTEN_FDS = int(os.environ.get("LISTEN_FDS", 0))
LISTEN_PID = os.environ.get("LISTEN_PID", None) or os.getpid()


# gets device status(known or unknown) if message received from ubertooth
async def device_status_u(device_name, ignore_uap):
    device_known = False
    device_nickname = "Unknown Device"
    # checks all sections(devices) in configparser to see if macaddr detected is equal
    for section in devices.sections():
        macaddr = devices.get(section, 'device_macaddr')
        if macaddr[9:] == device_name[9:]:  # last 3 parts of macaddr should always be available, check if match
            if macaddr[6:] == device_name[6:]:  # if last 4 parts are readable and = to device, known
                device_known = True
                device_nickname = devices.get(section, 'device_nickname')
            elif (macaddr[6:8] == '??') & (ignore_uap == "false"):  # if second part is ?? and we choose not to ignore uap, known
                device_known = True
    return device_known, device_nickname


# determine whether the message requires notification
async def message_eligibility(dev_type, zone, device_known, nickname, macaddr, ubertoothName):
    eligibility = False
    monitor_unknown = not device_known & (zones.get(zone, 'alert_on_unrecognized') == 'true')
    monitor_known = device_known & (zones.get(zone, 'alert_on_recognized') == 'true')
    monitor = False
    if dev_type == 'BTLE':
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
async def send_message(zone, msg):
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
async def process_message(message):
    message_json = json.loads(message)
    zone = 'DEFAULT'
#    notify = False
    detected_by_uuid = message_json['ubertooth_serial_number']
    dev_type = 'BT'
    # Determine which zone has detected the device from the configured zones
    for section in zones.sections():
        if section != 'DEFAULT':
            if detected_by_uuid == zones.get(section, 'zone_uuid'):
                zone = section

    for i in range(0, len(message_json['scan_results'])):
        device_mac = message_json['scan_results'][i]['mac']
        try:
            ubertooth_name = message_json['scan_results'][i]['name'] + ": "
        except:  # TODO: narrow this exception clause to catch specific one where we can't obtain ubertooth_name value
            ubertooth_name = ""
        device_known, nickname = await device_status_u(device_mac, zones.get(zone, 'ignore_devices_with_unknown_uap'))
        sendMsg, msg = await message_eligibility(dev_type, zone, device_known, nickname, device_mac, ubertooth_name)
        if sendMsg:
            await send_message(zone, msg)


# Handle incoming connections and process received messages.
async def handle_connection(reader, writer):
    while True:
        message = await reader.read(message_max_size)  # Wait until data is available
        if not message:  # Quit the loop when we stop getting data
            break
        message = message.decode()
        await process_message(message)
        print(message, flush=True)  # Replace this with a function call to dispatch messages to the notification server.
    writer.close()


# Socket loop, handles incoming UNIX socket connections (TODO: Implement signal handling so socket is properly cleaned up)
async def unix_socket():
    server = None  # initialize server variable so its always defined.
    fd_socket = None  # initialize fd_socket variable so its always defined.
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
