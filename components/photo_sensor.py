from machine import Pin, ADC
from config import PHOTO_SENSOR_PIN


class PhotoSensor:

    def __init__(self):
        self._adc = ADC(Pin(PHOTO_SENSOR_PIN))
        self._adc.atten(ADC.ATTN_11DB)

    def read_raw(self):
        return self._adc.read_u16()

    def read_percent(self):
        return self.read_raw() * 100 / 65535
