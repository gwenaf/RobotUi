from machine import Pin
from config import BUTTON_PIN


class Button:

    def __init__(self):
        self._pin = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return self._pin.value() == 0

    def on_press(self, callback):
        self._pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)
