import network
import time
from config import WIFI_TIMEOUT, AP_SSID, AP_AUTHMODE

def connect(ssid, password, max_wait_time=WIFI_TIMEOUT):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

    while max_wait_time > 0:
        if sta_if.isconnected():
            return sta_if.ipconfig()[0]
        max_wait_time -= 1
        time.sleep(1)

    sta_if.active(False)
    return False

def start_ap(essid=AP_SSID):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    ap_if.config(essid=essid, authmode=AP_AUTHMODE)
    return ap_if.ifconfig()[0]

def get_current_state():
    sta = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)

    if sta.active() and sta.isconnected():
        return "WIFI", sta.ifconfig()[0]
    elif ap.active():
        return "AP", ap.ifconfig()[0]
    return None, None