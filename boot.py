import time
import json

from components.display import Display
from components.wifi import WiFi
from config import CONFIG_FILE

display = Display()
wifi = WiFi()


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"networks": [], "admin_pass": ""}


display.show_message("Booting...", "Please Wait!")
time.sleep(1)

config = load_config()
networks = config.get("networks", [])

if networks:
    display.show_message("Scanning...", "Known networks")
    known = wifi.scan_known(networks)

    if known:
        display.show_message("Connecting...", known["ssid"])
        ip = wifi.connect(known["ssid"], known["password"])

        if ip:
            display.show_message("WiFi Mode", ip)
        else:
            display.show_message("Conn. Failed", "Starting AP")
            time.sleep(2)
            ip = wifi.start_ap()
            display.show_message("AP Mode", ip)
    else:
        display.show_message("No known net", "Starting AP")
        ip = wifi.start_ap()
        display.show_message("AP Mode", ip)
else:
    display.show_message("No networks", "Starting AP")
    ip = wifi.start_ap()
    display.show_message("AP Mode", ip)
