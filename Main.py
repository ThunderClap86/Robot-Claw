#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyPS4Controller.controller import Controller
import threading
import time
from PCA9685 import PCA9685


class MyController(Controller):

    def __init__(self, queue=None, **kwargs):
        Controller.__init__(self, **kwargs)
        self.queue = queue
        self.left = 0
        self.right = 0
        self.forward = 0
        self.backward = 0
        self.close = 0
        self.open = 0
        self.up = 0
        self.down = 0
        self.rotateright = 0
        self.rotateleft = 0
        self.wristup = 0
        self.wristdown = 0

    def on_L3_up(self, value):
        self.forward = value * -1 / 32767.0
        self.backward = 0

    def on_L3_down(self, value):
        self.forward = 0
        self.backward = value / 32767.0

    def on_L3_left(self, value):
        self.left = value * -1 / 32767.0
        self.right = 0

    def on_L3_right(self, value):
        self.left = 0
        self.right = value / 32767.0

    def on_L3_x_at_rest(self):
        self.left = 0
        self.right = 0

    def on_L3_y_at_rest(self):
        self.forward = 0
        self.backward = 0

    def on_L2_press(self, value):
        self.close = (value + 32768) / 65535.0
        self.open = 0

    def on_L2_release(self):
        self.close = 0

    def on_R2_press(self, value):
        self.close = 0
        self.open = (value + 32768) / 65535.0

    def on_R2_release(self):
        self.open = 0

    def on_R3_up(self, value):
        self.up = value * -1 / 32768.0
        self.down = 0

    def on_R3_down(self, value):
        self.up = 0
        self.down = value / 32767.0

    def on_R3_y_at_rest(self):
        self.up = 0
        self.down = 0

    def on_R3_left(self, value):
        self.wristup = 0
        self.wristdown = value / 32767.0

    def on_R3_right(self, value):
        self.wristup = value / 32767.0
        self.wristdown = 0

    def on_R3_x_at_rest(self):
        self.wristup = 0
        self.wristdown = 0

    def on_right_arrow_press(self, value):
        self.rotateright = (value + 32768) / 65535.0
        self.rotateleft = 0

    def on_right_arrow_release(self):
        self.rotateright = 0

    def on_left_arrow_press(self, value):
        self.rotateright = 0
        self.rotateleft = (value + 32768) / 65535.0

    def on_left_arrow_release(self):
        self.rotateleft = 0


class RoboArt(threading.Thread):

    S3_CLOSED = 500
    S3_OPEN = 2000
    S0_IN = 600
    S0_OUT = 2000
    S2_LEFT = 500
    S2_RIGHT = 2000
    S1_HIGH = 3000
    S1_LOW = 200
    S4_ROTATERIGHT = 3000
    S4_ROTATELEFT = 500
    S5_WRISTUP = 3000
    S5_WRISTDOWN = 500

    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.driver = PCA9685(0x40, debug=False)
        self.driver.setPWMFreq(50)
        self._lock = threading.Lock()
        self.controller = controller

    def check(
        self,
        s0,
        s1,
        s2,
        s3,
        s4,
        s5,
        ):

        if s3 > RoboArt.S3_OPEN:
            s3 = RoboArt.S3_OPEN
        if s3 < RoboArt.S3_CLOSED:
            s3 = RoboArt.S3_CLOSED
        if s2 > RoboArt.S2_RIGHT:
            s2 = RoboArt.S2_RIGHT
        if s2 < RoboArt.S2_LEFT:
            s2 = RoboArt.S2_LEFT
        if s0 > RoboArt.S0_OUT:
            s0 = RoboArt.S0_OUT
        if s0 < RoboArt.S0_IN:
            s0 = RoboArt.S0_IN
        if s1 > RoboArt.S1_HIGH:
            s1 = RoboArt.S1_HIGH
        if s1 < RoboArt.S1_LOW:
            s1 = RoboArt.S1_LOW
        if s4 > RoboArt.S4_ROTATERIGHT:
            s4 = RoboArt.S4_ROTATERIGHT
        if s4 < RoboArt.S4_ROTATELEFT:
            s4 = RoboArt.S4_ROTATELEFT
        if s5 > RoboArt.S5_WRISTUP:
            s5 = RoboArt.S5_WRISTUP
        if s5 < RoboArt.S5_WRISTDOWN:
            s5 = RoboArt.S5_WRISTDOWN
        return (
            s0,
            s1,
            s2,
            s3,
            s4,
            s5,
            )

    def run(self):
        servo0 = 1000
        servo1 = 1320
        servo2 = 1000
        servo3 = 1000
        servo4 = 1000
        servo5 = 1000

        while True:
            if controller.open > 0:
                servo3 -= int(50 * controller.open)
            elif controller.close:
                servo3 += int(50 * controller.close)
            if controller.left > 0:
                servo2 += int(25 * controller.left)
            elif controller.right > 0:
                servo2 -= int(25 * controller.right)
            if controller.up > 0:
                servo1 -= int(25 * controller.up)
            elif controller.down > 0:
                servo1 += int(25 * controller.down)
            if controller.forward > 0:
                servo0 += int(25 * controller.forward)
            elif controller.backward > 0:
                servo0 -= int(25 * controller.backward)
            if controller.wristup > 0:
                servo5 -= int(25 * controller.wristup)
            elif controller.wristdown > 0:
                servo5 += int(25 * controller.wristdown)
            if controller.rotateleft > 0:
                servo4 += int(25 * controller.rotateleft)
            elif conroller.rotateright > 0:
                servo4 -= int(25 * controller.rotateright)

            (
                servo0,
                servo1,
                servo2,
                servo3,
                servo4,
                servo5,
                ) = self.check(
                servo0,
                servo1,
                servo2,
                servo3,
                servo4,
                servo5,
                )
            self.driver.setServoPulse(0, servo0)
            self.driver.setServoPulse(1, servo1)
            self.driver.setServoPulse(2, servo2)
            self.driver.setServoPulse(3, servo3)
            self.driver.setServoPulse(4, servo4)
            self.driver.setServoPulse(5, servo5)
            time.sleep(0.025)


controller = MyController(interface='/dev/input/js0',
                          connecting_using_ds4drv=False)
arm = RoboArt(controller)
arm.start()
controller.listen(timeout=60)