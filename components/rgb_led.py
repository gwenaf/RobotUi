from machine import Pin
from config import RGB_RED_PIN, RGB_GREEN_PIN, RGB_BLUE_PIN


class RgbLed:
    """Digital RGB LED (on/off per channel, no PWM needed)."""

    def __init__(self):
        self._red = Pin(RGB_RED_PIN, Pin.OUT, value=0)
        self._green = Pin(RGB_GREEN_PIN, Pin.OUT, value=0)
        self._blue = Pin(RGB_BLUE_PIN, Pin.OUT, value=0)

    def set_color(self, r, g, b):
        self._red.value(1 if r > 127 else 0)
        self._green.value(1 if g > 127 else 0)
        self._blue.value(1 if b > 127 else 0)

    def off(self):
        self._red.value(0)
        self._green.value(0)
        self._blue.value(0)
