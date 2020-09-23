#!/usr/bin/python3

import os
import asyncio

# Begin Script Constants Definition
message_socket_path = '/run/bt-surveillance-processing.sock'  # Path and name of the listening socket.
message_socket = None  # Actual socket we'll be getting messages from. Initialized to None until socket is setup.
message_socket_permissions = 0o666  # Socket Permissions, see note in setup function for more info.
message_max_size = 1024  # Max size of single message in bytes. Anything longer is truncated. Must be power of 2
# End Script Constants Definition


# Begin Script Functions Definition
# Handle incoming connections and process received messages.
async def handle_connection(reader, writer):
    while True:
        message = await reader.read(message_max_size)  # Wait until data is available
        if not message:  # Quit the loop when we stop getting data
            break
        message = message.decode()
        print(message)  # Replace this with a function call to dispatch messages to the notification server.
    writer.close()


# Main loop, runs until process is shutdown (TODO: Implement signal handling so socket is properly cleaned up)
async def main():
    # Detect if socket file already exists and clean it up if it does
    if os.path.exists(message_socket_path):
        os.unlink(message_socket_path)
    server = await asyncio.start_unix_server(handle_connection, path=message_socket_path, start_serving=False)
    os.chmod(message_socket_path, message_socket_permissions)
    async with server:
        await server.serve_forever()

# End Script Functions Definition


# Begin Main Script Invocation
asyncio.run(main())  # This just spins up the async main loop we defined earlier.
# End Main Script Invocation
