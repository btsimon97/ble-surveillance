import requests
import json
kismet_host = "localhost:2501"
kismet_api_path = "devices/views/phy-BTLE/last-time/"
device_last_activity_timeout = 60


api_username='kismet'
api_password='kismet'
device_api_args = 'json={"fields": ["btle.device","kismet.device.base.commonname","kismet.device.base.first_time","kismet.device.base.last_time","kismet.device.base.mod_time"]}'
device_api_url = "http://" + kismet_host + "/" + kismet_api_path + "-" + str(device_last_activity_timeout) + "/devices.json"

x = requests.post(device_api_url,data=device_api_args,headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},auth=(api_username,api_password))
print(json.dumps(x.json(),indent=2))
