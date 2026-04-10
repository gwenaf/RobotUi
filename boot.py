import time
import json
import network

from components.display import show_message
from components.wifi import start_ap, connect
from config import CONFIG_FILE

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except OSError:
        return {"ssid": "", "password": "", "admin_pass": ""}

show_message("Booting...", "Please Wait!")
time.sleep(1);

config = load_config()

if config.get("ssid", "") == "":
    show_message("No WiFi found !", "Starting AP Mode")
    ip = wifi.start_ap()
    show_message("AP Mode", ip)
else:
    show_message("WiFi found!", config["ssid"])
    ip = wifi.connect(config["ssid"], config["password"])

    if ip:
        show_message("WiFi Mode", ip)
    else:
        show_message("Conn. Failed", "Start. AP Mode")
        time.sleep(2)
        ip = wifi.start_ap()
        show_message("AP Mode", ip)