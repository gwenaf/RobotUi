import network
import time
from config import WIFI_TIMEOUT, AP_SSID, AP_AUTHMODE


class WiFi:

    def __init__(self):
        self._sta = network.WLAN(network.STA_IF)
        self._ap = network.WLAN(network.AP_IF)

    def scan(self):
        self._sta.active(True)
        return [net[0].decode() for net in self._sta.scan()]

    def scan_known(self, networks):
        available = self.scan()
        for net in networks:
            if net["ssid"] in available:
                return net
        return None

    def connect(self, ssid, password, timeout=WIFI_TIMEOUT):
        self._sta.active(True)
        self._sta.connect(ssid, password)

        while timeout > 0:
            if self._sta.isconnected():
                return self._sta.ifconfig()[0]
            timeout -= 1
            time.sleep(1)

        self._sta.active(False)
        return False

    def start_ap(self, essid=AP_SSID):
        self._ap.active(True)
        self._ap.config(essid=essid, authmode=AP_AUTHMODE)
        return self._ap.ifconfig()[0]

    def get_current_state(self):
        if self._sta.active() and self._sta.isconnected():
            return "WIFI", self._sta.ifconfig()[0]
        elif self._ap.active():
            return "AP", self._ap.ifconfig()[0]
        return None, None
