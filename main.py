from boot import display, wifi
from components.motors import Motors
from components.ultrasound import UltrasoundSensor
from components.photo_sensor import PhotoSensor
from components.rgb_led import RgbLed
from components.serial_led import SerialLed
from components.accelerometer import Accelerometer
import server

if __name__ == '__main__':
    mode, ip = wifi.get_current_state()
    display.show_message(f"{mode} - Ready", ip or "No connection")

    components = {}

    try:
        components['motors'] = Motors()
    except Exception as e:
        print("Motors init failed:", e)

    try:
        components['ultrasound'] = UltrasoundSensor()
    except Exception as e:
        print("Ultrasound init failed:", e)

    try:
        components['photo'] = PhotoSensor()
    except Exception as e:
        print("PhotoSensor init failed:", e)

    try:
        components['rgb'] = RgbLed()
    except Exception as e:
        print("RgbLed init failed:", e)

    try:
        components['serial'] = SerialLed()
    except Exception as e:
        print("SerialLed init failed:", e)

    try:
        components['accel'] = Accelerometer(i2c=display.i2c)
    except Exception as e:
        print("Accelerometer init failed:", e)

    server.start(display, wifi, components)
