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


async def kismet_websocket(configuration):
    uri = ""
    ssl_context = None # Used for TLS websocket sessions, initialized here so it can be setup later.

    # message sent to kismet to get device data, along with some field simplification to reduce the data we get back.
    # split across multiple lines for better visibility.
    subscription_message = '{"SUBSCRIBE": "NEW_DEVICE", "fields":["kismet.device.base.seenby","kismet.device.base.macaddr","kismet.device.base.commonname","kismet.device.base.type"]}'

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