from machine import Pin, I2C
from lib import ssd1306
from config import OLED_SCL_PIN, OLED_SDA_PIN, OLED_I2C_FREQ_HZ, OLED_WIDTH, OLED_HEIGHT

i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=OLED_I2C_FREQ_HZ)

oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

def show_message(line1, line2=""):
    oled.fill(0)
    oled.text(line1, 0,0)
    oled.text(line2, 0,16)
    oled.show()