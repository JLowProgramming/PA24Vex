#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
mc55_10 = Motor55(Ports.PORT10, False)
mc55_20 = Motor55(Ports.PORT20, False)
servo_a = Servo(brain.three_wire_port.a)
servo_h = Servo(brain.three_wire_port.h)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       sethe                                                        #
# 	Created:      10/24/2024, 5:18:31 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

claw_open = False
claw_pos_right = 0
claw_pos_left = 0
min_claw_pos_left = 0
max_claw_pos_left = 90
min_claw_pos_right = -90
max_claw_pos_right = 0

# Brain should be defined by default

brain=Brain()

#Assigning motors to ports
controller_1 = Controller(PRIMARY)
left_motor = Motor55(Ports.PORT10, True)
right_motor = Motor55(Ports.PORT20, True)
arm_motor = Motor55(Ports.PORT1)
right_servo = Servo(brain.three_wire_port.h)
left_servo = Servo(brain.three_wire_port.a)

#Sets the motors to constantly spin, velocities are changed with the rest of the script.
left_motor.spin(FORWARD)
right_motor.spin(FORWARD)
arm_motor.spin(FORWARD)


def set_left_claw(deg):
    global claw_pos_left
    left_servo.set_position(deg) 
    claw_pos_left = deg

def set_right_claw(deg):
    global claw_pos_right
    right_servo.set_position(deg) 
    claw_pos_right = deg

def close_claw():
    global claw_pos_right
    global claw_pos_left
    while controller_1.buttonL2.pressing() and claw_pos_left <= max_claw_pos_left and claw_pos_right >= min_claw_pos_right:
        set_left_claw(claw_pos_left + 1)
        set_right_claw(claw_pos_right - 1)
        wait(.01, SECONDS)
def open_claw():
    global claw_pos_right
    global claw_pos_left
    while controller_1.buttonL1.pressing() and claw_pos_left >= min_claw_pos_left and claw_pos_right <= max_claw_pos_right:
        set_left_claw(claw_pos_left - 1)
        set_right_claw(claw_pos_right + 1)
        wait(.01, SECONDS)

controller_1.buttonL2.pressed(close_claw)
controller_1.buttonL1.pressed(open_claw)

while True:
    left_motor.set_velocity(controller_1.axis4.position() + controller_1.axis3.position())
    right_motor.set_velocity(controller_1.axis4.position() - controller_1.axis3.position())
    arm_motor.set_velocity(1 if controller_1.buttonR1.pressing() else (-1 if controller_1.button_R2.pressing() else 0))
