from machine import Pin
from neopixel import NeoPixel
from config import SERIAL_LED_PIN, SERIAL_LED_COUNT


class SerialLed:

    def __init__(self):
        self._np = NeoPixel(Pin(SERIAL_LED_PIN), SERIAL_LED_COUNT)

    def set(self, index, r, g, b):
        self._np[index] = (r, g, b)
        self._np.write()

    def set_all(self, r, g, b):
        for i in range(SERIAL_LED_COUNT):
            self._np[i] = (r, g, b)
        self._np.write()

    def off(self):
        self.set_all(0, 0, 0)
