from machine import Pin, I2C
from lib import ssd1306
from config import (OLED_SCL_PIN, OLED_SDA_PIN, OLED_I2C_FREQ_HZ,
                    OLED_WIDTH, OLED_HEIGHT)


class Display:

    def __init__(self):
        self.i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN),
                       freq=OLED_I2C_FREQ_HZ)
        self._oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, self.i2c)

    def show_message(self, line1, line2=""):
        self._oled.fill(0)
        self._oled.text(line1, 0, 0)
        self._oled.text(line2, 0, 16)
        self._oled.show()

    def clear(self):
        self._oled.fill(0)
        self._oled.show()
