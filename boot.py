import time
import json
import network

from components.display import show_message, show_ip

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except OSError:
        return {"ssid": "", "password": "", "admin_pass": ""}

def connect_to_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

    # 10 second waiting for the handshake
    max_wait_time = 10 #seconds
    while max_wait_time > 0:
        if sta_if.isconnected():
            return sta_if.ifconfig()[0]
        max_wait_time -= 1
        time.sleep(1)

    # If the connection fails
    sta_if.active(False)
    return False

def start_access_point():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)

    ap_if.config(essid="Robot-Setup", authmode=0)
    return ap_if.ifconfig()[0]

show_message("Booting...", "Init system")
time.sleep(1)

config = load_config()
ip_address = False
current_mode = ""

if config["ssid"] == "":
    show_message("No WiFi", "Conf. Required!")
    ip_address = start_access_point()
    current_mode = "AP"
else:
    show_message("WiFi found:", config["ssid"])
    ip_address = connect_to_wifi(config["ssid"], config["password"])
    if ip_address:
        current_mode = "WIFI"

show_ip(current_mode, ip_address)