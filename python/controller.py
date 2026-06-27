import pygame
import serial
import time
import ik
from ik import Motors
from dataclasses import dataclass

@dataclass
class allMotors:
    base: int = 90.0
    shoulder: int = 90.0
    elbow: int = 90.0
    wrist: int = 90.0
    wristr: int = 90.0
    gripper: int = 90.0

def dead_zone(x):
    deadzone = 0.1
    if abs(x) < deadzone:
        return 0
    return x

def read_buttons():
    global L3x, L3y, R3x, R3y, Lt, Rt, lb, rb, dpad
    pygame.event.pump()
    L3x = dead_zone(controller.get_axis(0))
    L3y = dead_zone(controller.get_axis(1))
    R3x = dead_zone(controller.get_axis(2))
    R3y = dead_zone(controller.get_axis(3))

    Lt = dead_zone(controller.get_axis(5))
    Rt = dead_zone(controller.get_axis(4))

    lb = controller.get_button(6)
    rb = controller.get_button(7)
    dpad = controller.get_hat(0)

   # print(f"L3x:{L3x}, L3y:{L3y}, R3x:{R3x}, R3y:{R3y}, lb:{lb}, rb:{rb}, lt:{Lt}, rt:{Rt}, dpad:{dpad}")

def clamp(x):
    if x > 180:
        return 180
    if x < 0:
        return 0
    return x

def trigger_active(raw_value, invert_mode):
    if invert_mode:
        return raw_value < 0.5
    mapped = (raw_value + 1.0) / 2.0 if raw_value < 0 else raw_value
    return mapped > 0.6

def chords(motors):
    global x, y, prev_rt_active, prev_lt_active
    x += L3x * 10
    if x < -245:
        x = -245
    if x > 245:
        x = 245

    y -= L3y * 10
    if y > 245:
        y = 245
    if y < -102:
        y = -102

    # base from shoulder buttons
    if rb != 0:
        motors.base -=  2
    if lb != 0:
        motors.base +=  2

    # wrist controls
    motors.wrist += R3y * 10
    motors.wristr += R3x * 10

    # gripper controls (edge triggered): one command per press
    rt_is_active = trigger_active(Rt, rt_invert)
    lt_is_active = trigger_active(Lt, lt_invert)

    if rt_is_active and not prev_rt_active and not lt_is_active:
        motors.gripper = 80
    elif lt_is_active and not prev_lt_active and not rt_is_active:
        motors.gripper = 180

    prev_rt_active = rt_is_active
    prev_lt_active = lt_is_active

    motors.base = clamp(motors.base)
    motors.wrist = clamp(motors.wrist)
    motors.wristr = clamp(motors.wristr)
    motors.gripper = clamp(motors.gripper)

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=0.2, write_timeout=0.2)
time.sleep(2)


pygame.init()
pygame.joystick.init()
gamepad_count = pygame.joystick.get_count()
if gamepad_count == 0:
    print("No gamepads found")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()
motors = allMotors()

x = 0
y = 245
last_message = ""
prev_rt_active = False
prev_lt_active = False

# trigger baseline calibration (supports controllers where trigger rest is ~1.0)
read_buttons()
rt_invert = Rt > 0.8
lt_invert = Lt > 0.8

while 1:
    read_buttons()
    
    chords(motors)

    # keep your IK call as implemented in your ik module
    elbow_shoulder: Motors = ik.ik(x, y)  # if this errors, change to ik.ik(x, y)
    motors.elbow = elbow_shoulder.elbow
    motors.shoulder = elbow_shoulder.shoulder

    message = f"{int(motors.base)},{int(motors.shoulder)},{int(motors.elbow)},{int(motors.wrist)},{int(motors.wristr)},{int(motors.gripper)}\n"
    if message != last_message:
        ser.write(message.encode("utf-8"))
        ser.readline()
        last_message = message

    #print(f"x{x}, y{y}:")
    #print(message)
    #print(f"base:{motors.base}, shoulder:{motors.shoulder}, elbow:{motors.elbow}, wrist:{motors.wrist}, wrist rotation:{motors.wristr}, griper:{motors.gripper}")
    time.sleep(0.02)


