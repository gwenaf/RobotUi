from machine import Pin, I2C
from lib.MPU6050_my_library import MPU6050
from config import ACCELEROMETER_SDA_PIN, ACCELEROMETER_SCL_PIN, OLED_I2C_FREQ_HZ
import time


class Accelerometer:

    def __init__(self, i2c=None):
        if i2c is None:
            i2c = I2C(0, sda=Pin(ACCELEROMETER_SDA_PIN),
                       scl=Pin(ACCELEROMETER_SCL_PIN), freq=400000)
        self._mpu = MPU6050(i2c)
        self._gyro_z_offset = 0.0
        self._mpu.sleep_mode_activation(False)

    def configure(self, dlpf=3, sample_rate_div=10, gyro_range=3, accel_range=3):
        self._mpu.change_digital_low_pass_filter_setting(dlpf)
        self._mpu.change_sample_rate_divider(sample_rate_div)
        self._mpu.change_gyroscope_full_scale_range(gyro_range)
        self._mpu.change_accelerometer_full_scale_range(accel_range)

    def enable_fifo(self):
        self._mpu.change_fifo_enable_settings(
            temp=False,
            gyroscope_x_axis=True,
            gyroscope_y_axis=True,
            gyroscope_z_axis=True,
            accelerometer=True
        )

    def calibrate_gyro_z(self, samples=200):
        values = []
        for _ in range(samples):
            data = self._mpu.read_all_sensors()
            values.append(data["gz"])
            time.sleep_ms(10)
        self._gyro_z_offset = sum(values) / len(values)
        return self._gyro_z_offset

    def read_all(self):
        return self._mpu.read_all_sensors()

    def read_fifo(self):
        return self._mpu.read_data_from_fifo_register()

    @property
    def gyro_z_offset(self):
        return self._gyro_z_offset
