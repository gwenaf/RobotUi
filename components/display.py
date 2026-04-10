from machine import Pin, I2C
from lib import ssd1306

i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=100000)

oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def show_message(line1, line2=""):
    oled.fill(0)
    oled.text(line1, 0,0)
    oled.text(line2, 0,16)
    oled.show()

def show_ip(mode, ip):
    oled.fill(0)
    oled.text(f"Mode : {mode}", 0, 0)
    oled.text(ip, 0, 16)
    oled.show()