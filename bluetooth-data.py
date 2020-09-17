import requests
import json
import configparser
import datetime
import time

# Read in the config file (this needs to get changed when a production ready version is made)
config = configparser.ConfigParser()
config.read('ble-surveillance.conf')


def validate_config_file(configuration):
    if 'kismet' not in configuration:
        raise SyntaxError("Config file is missing the kismet section")
    # TODO: Add more config file validation code


def build_api_base_url(configuration):
    # Pull the hostname and port of the Kismet server from config
    api_host = configuration['kismet']['server_name']
    api_port = configuration['kismet']['server_port']
    # If configured to use HTTPS, format URL as such
    if configuration['kismet'].getboolean('use_tls'):
        url = "https://" + api_host + ":" + api_port
        return url
    # Return plain HTTP when HTTPS not enabled.
    else:
        url = "http://" + api_host + ":" + api_port
        return url


def get_device_api_paths(url, configuration):
    # Kismet API path that lists all available device views
    device_api_discovery_path = "/devices/views/all_views.json"
    x = requests.get(url+device_api_discovery_path,
                     auth=(configuration['kismet']['username'], configuration['kismet']['password']))
    return x.json()


def get_bluetooth_api_paths(url, configuration):
    device_api_paths = get_device_api_paths(url,configuration)
    filtered_endpoints = [x for x in device_api_paths
                          if (("Bluetooth" in x['kismet.devices.view.description'])
                              or ("BTLE" in x['kismet.devices.view.description']))]
    return filtered_endpoints


def get_devices(url, device_api_endpoints, configuration):
    device_api_args = 'json={"fields": ["kismet.device.base.commonname","kismet.device.base.first_time",' \
                      '"kismet.device.base.last_time","kismet.device.base.mod_time"]}'

    device_lists = []  # create python list to store the device lists (a list of lists)
    for endpoint in device_api_endpoints:
        device_api_url = url + "/devices/views/" + endpoint['kismet.devices.view.id'] + "/last-time/" + "-" \
                         + configuration['kismet']['active_device_timeout'] + "/devices.json"
        x = requests.post(device_api_url, data=device_api_args,
                          headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
                          auth=(configuration['kismet']['username'], configuration['kismet']['password']))
        device_lists.append(x.json())  # add the device list to the list of device lists

    device_list = []  # create python list to store consolidated device list
    for dev_list in device_lists:  # consolidate the device lists into single device lists
        device_list += dev_list

    return device_list


def get_new_devices(device_list, last_probe_time):
    if last_probe_time == 0:  # On initial probe of API, all devices are new.
        return device_list
    else:
        new_devices = []
        for device in device_list:  # iterate over the entire device list
            # if the device appeared after the last time we probed (>= since timestamp changes after probe completes)
            if datetime.datetime.fromtimestamp(device['kismet.device.base.first_time'], tz=None) >= last_probe_time:
                new_devices.append(device)  # add the device to the new devices list
        return new_devices  # return the newly discovered devices


# initialize the API URL and other important constants that will be reused
api_url = build_api_base_url(config)
bluetooth_api_endpoints = get_bluetooth_api_paths(api_url, config)

# get devices active in the last X seconds (governed by the active_device_timeout option in the config)
devices = get_devices(api_url, bluetooth_api_endpoints, config)
# get the list of "fresh" devices (those newly discovered, all of them since this is our first probe)
fresh_devices = get_new_devices(devices, 0)
# print the list of "fresh" devices to console (replace this with notification code)
print(json.dumps(fresh_devices, indent=2))
# set the last API probe time to now (we need to have this so we can tell what devices are newly detected)
last_api_probe = datetime.datetime.now()

# loop forever until terminated
while True:
    time.sleep(config.getint('kismet', 'api_probe_interval'))  # sleep until probe interval has passed
    devices = get_devices(api_url, bluetooth_api_endpoints, config)  # refresh the list of all devices
    fresh_devices = get_new_devices(devices, last_api_probe)  # get the list of devices that are new since last probe
    print(json.dumps(fresh_devices, indent=2)) # print new devices to console (replace with notification code)
    last_api_probe = datetime.datetime.now()  # update last probe timestamp to be now since we just finished a probe
