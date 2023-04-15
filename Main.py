import pygame
import time
from adafruit_pca9685 import PCA9685

# Set up the PCA9685
pca = PCA9685()
pca.frequency = 50

# Set up the servo channels
servo_channel_1 = 0
servo_channel_2 = 1
servo_channel_3 = 2
servo_channel_4 = 3
servo_channel_5 = 4
servo_channel_6 = 5

# Set up the servo min/max values (in microseconds)
servo_min = 1000
servo_max = 2000

# Set up the controller
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Function to map joystick values to servo values
def map_joystick_to_servo(joystick_value, servo_min, servo_max):
    servo_range = servo_max - servo_min
    mapped_value = int((joystick_value + 1) / 2 * servo_range + servo_min)
    return mapped_value

# Main loop
try:
    while True:
        # Get the joystick events
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
                # Get the joystick values
                left_stick_x = joystick.get_axis(0)
                left_stick_y = joystick.get_axis(1)
                right_stick_x = joystick.get_axis(2)
                right_stick_y = joystick.get_axis(3)
                L1 = joystick.get_button(4)
                R1 = joystick.get_button(5)
                L2 = joystick.get_axis(2)
                R2 = joystick.get_axis(5)
                
                # Map the joystick values to servo values
                mapped_left_stick_y = map_joystick_to_servo(-left_stick_y, servo_min, servo_max)
                mapped_right_stick_y = map_joystick_to_servo(-right_stick_y, servo_min, servo_max)
                mapped_left_stick_x = map_joystick_to_servo(left_stick_x, servo_min, servo_max)
                mapped_right_stick_x = map_joystick_to_servo(right_stick_x, servo_min, servo_max)
                mapped_L1 = map_joystick_to_servo(L1, servo_min, servo_max)
                mapped_R1 = map_joystick_to_servo(R1, servo_min, servo_max)
                mapped_L2 = map_joystick_to_servo(L2, servo_min, servo_max)
                mapped_R2 = map_joystick_to_servo(R2, servo_min, servo_max)
                
                # Set the servo values based on the joystick values
                pca.channels[servo_channel_1].duty_cycle = mapped_L1
                pca.channels[servo_channel_6].duty_cycle = mapped_R1
                pca.channels[servo_channel_2].duty_cycle = mapped_left_stick_y
                pca.channels[servo_channel_3].duty_cycle = mapped_right_stick_y
                pca.channels[servo_channel_4].duty_cycle = mapped_left_stick_x
                pca.channels[servo_channel_5].duty_cycle = mapped_right_stick_x
except KeyboardInterrupt:
    joystick.quit()
