import time
import json

from components.display import show_message
from components.wifi import scan_known, connect, start_ap
from config import CONFIG_FILE


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"networks": [], "admin_pass": ""}


show_message("Booting...", "Please Wait!")
time.sleep(1)

config = load_config()
networks = config.get("networks", [])

if networks:
    show_message("Scanning...", "Known networks")
    known = scan_known(networks)

    if known:
        show_message("Connecting...", known["ssid"])
        ip = connect(known["ssid"], known["password"])

        if ip:
            show_message("WiFi Mode", ip)
        else:
            show_message("Conn. Failed", "Starting AP")
            time.sleep(2)
            ip = start_ap()
            show_message("AP Mode", ip)
    else:
        show_message("No known net", "Starting AP")
        ip = start_ap()
        show_message("AP Mode", ip)
else:
    show_message("No networks", "Starting AP")
    ip = start_ap()
    show_message("AP Mode", ip)
