from machine import Pin, time_pulse_us
import time
from config import ULTRASOUND_SENSOR_TR_PIN, ULTRASOUND_SENSOR_EC_PIN


class UltrasoundSensor:

    def __init__(self):
        self._trigger = Pin(ULTRASOUND_SENSOR_TR_PIN, Pin.OUT)
        self._echo = Pin(ULTRASOUND_SENSOR_EC_PIN, Pin.IN)
        self._trigger.value(0)

    def distance_cm(self):
        self._trigger.value(0)
        time.sleep_us(2)
        self._trigger.value(1)
        time.sleep_us(10)
        self._trigger.value(0)

        duration = time_pulse_us(self._echo, 1, 30000)
        if duration < 0:
            return -1
        return duration * 0.0343 / 2
