from machine import Pin, PWM
from config import (MOTOR_LEFT_F, MOTOR_LEFT_R,
                    MOTOR_RIGHT_F, MOTOR_RIGHT_R, MOTOR_PWM_FREQ)


class Motors:

    def __init__(self):
        self._lf = PWM(Pin(MOTOR_LEFT_F), freq=MOTOR_PWM_FREQ, duty_u16=0)
        self._lr = PWM(Pin(MOTOR_LEFT_R), freq=MOTOR_PWM_FREQ, duty_u16=0)
        self._rf = PWM(Pin(MOTOR_RIGHT_F), freq=MOTOR_PWM_FREQ, duty_u16=0)
        self._rr = PWM(Pin(MOTOR_RIGHT_R), freq=MOTOR_PWM_FREQ, duty_u16=0)

    @staticmethod
    def _pct_to_duty(pct):
        value = int(pct * 65535 / 100)
        return max(0, min(65535, value))

    # --- Per-wheel control ---

    def left_forward(self, speed):
        self._lf.duty_u16(self._pct_to_duty(speed))
        self._lr.duty_u16(0)

    def left_backward(self, speed):
        self._lf.duty_u16(0)
        self._lr.duty_u16(self._pct_to_duty(speed))

    def left_stop(self):
        self._lf.duty_u16(0)
        self._lr.duty_u16(0)

    def left_brake(self):
        self._lf.duty_u16(65535)
        self._lr.duty_u16(65535)

    def right_forward(self, speed):
        self._rf.duty_u16(self._pct_to_duty(speed))
        self._rr.duty_u16(0)

    def right_backward(self, speed):
        self._rf.duty_u16(0)
        self._rr.duty_u16(self._pct_to_duty(speed))

    def right_stop(self):
        self._rf.duty_u16(0)
        self._rr.duty_u16(0)

    def right_brake(self):
        self._rf.duty_u16(65535)
        self._rr.duty_u16(65535)

    # --- High-level control ---

    def forward(self, speed=50):
        self.left_forward(speed)
        self.right_forward(speed)

    def backward(self, speed=50):
        self.left_backward(speed)
        self.right_backward(speed)

    def turn_left(self, speed=50):
        self.left_backward(speed)
        self.right_forward(speed)

    def turn_right(self, speed=50):
        self.left_forward(speed)
        self.right_backward(speed)

    def stop(self):
        self.left_stop()
        self.right_stop()

    def brake(self):
        self.left_brake()
        self.right_brake()
