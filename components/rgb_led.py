from machine import Pin, PWM
from config import RGB_RED_PIN, RGB_GREEN_PIN, RGB_BLUE_PIN


class RgbLed:

    def __init__(self):
        self._red = PWM(Pin(RGB_RED_PIN), freq=1000, duty_u16=0)
        self._green = PWM(Pin(RGB_GREEN_PIN), freq=1000, duty_u16=0)
        self._blue = PWM(Pin(RGB_BLUE_PIN), freq=1000, duty_u16=0)

    def set_color(self, r, g, b):
        self._red.duty_u16(r * 257)
        self._green.duty_u16(g * 257)
        self._blue.duty_u16(b * 257)

    def off(self):
        self.set_color(0, 0, 0)
