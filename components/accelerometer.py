from machine import Pin, I2C
from lib.mpu6050 import MPU6050
from config import ACCELEROMETER_SDA_PIN, ACCELEROMETER_SCL_PIN


class Accelerometer:

    def __init__(self, i2c=None):
        if i2c is None:
            i2c = I2C(0, sda=Pin(ACCELEROMETER_SDA_PIN),
                       scl=Pin(ACCELEROMETER_SCL_PIN), freq=400000)
        self._mpu = MPU6050(i2c)

    def read_all(self):
        vals = self._mpu.get_values()
        # Remap: chip X=left, Y=forward, Z=down → robot X=forward, Y=right, Z=up
        return {
            'ax': vals['AcY'],
            'ay': -vals['AcX'],
            'az': -vals['AcZ'],
            'gx': vals['GyY'],
            'gy': -vals['GyX'],
            'gz': -vals['GyZ'],
            'temp': vals['Tmp']
        }
