#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.tools import wait
#from pixycamev3.pixy2 import Pixy2, MainFeatures

ev3 = EV3Brick()
#pixy2 = Pixy2(port = 1, i2c_address = 0x54)
motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steering = Motor(Port.A)
#ir = InfraredSensor(Port.S1)
cs = ColorSensor(Port.S2)
gs = GyroSensor(Port.S1)
watch = StopWatch()



""" UTILS """

def getDistance():
    return ir.distace()

def getColor():
    print("Color:", cs.color())
    return cs.color()

def getAngle():
    global quarterLap
    print("Angle:", gs.angle()/quarterLap)
    return gs.angle() / quarterLap            #Switch Return(s)
    #return 90  / quarterLap

def goStraightOn():
    global steeringSpeed, lastCorrection
    steering.run_angle(steeringSpeed, -lastCorrection, wait = True)
    correction = -getAngle()
    lastCorrection = correction
    print("Correction:", correction)
    steering.run_angle(steeringSpeed, correction, wait = False)

def turnBlueLine():
    global steeringSpeed, flag_line, quarterLap
    currentSteeringAngle = steering.angle()
    steering.run_angle( steeringSpeed, -currentSteeringAngle, wait = True) # Closing (If there's something opened or a value to correct)
    flag_line = True
    steeringAngle = 30
    steering.run_angle(steeringSpeed, steeringAngle, wait = False) # Opening
    while (getAngle() < 88):
        wait(100)
    steering.run_angle(steeringSpeed, -steeringAngle, wait = False) # Closing
    quarterLap = quarterLap + 1

def turnOrangeLine():
    global steeringSpeed, flag_line, quarterLap
    currentSteeringAngle = steering.angle()
    print("Current steering angle:", currentSteeringAngle)
    steering.run_angle( steeringSpeed, -currentSteeringAngle, wait = True) # Closing (If there's something opened or a value to correct)
    flag_line = True
    steeringAngle = -10
    steering.run_angle(steeringSpeed, steeringAngle, wait = False) # Opening
    while (getAngle() > -88):
        wait(100)
    steering.run_angle(steeringSpeed, -steeringAngle, wait = False) # Closing
    quarterLap = quarterLap + 1

def takeAnAction():
    global action
    if (action == "moveStraight"):
        goStraightOn()
    elif (action == "onOrangeLine"):
        turnOrangeLine()
    elif (action == "onBlueLine"):
        turnBlueLine()
    action = ""




""" ALGORITHM """

# Avvio la propulsione
motor.run(1000)

# Initializations
steeringSpeed = 25
motorSpeed = 1000
watch.reset()
gs.reset_angle(0)
flag_line = False
blocks = False
lastCorrection = 0
quarterLap = 1
lapCompleted = 0
action = ""
# Ciclo equivalente al loop() di uno sketch Arduino
while True:

    # Acquiring information
    color = getColor()

    # Color Lines
    if (color == Color.RED):
        action = "onOrangeLine"
    elif (color == Color.BLUE):
        action = "onBlueLine"
    # Pixy
    elif (blocks):
        pass
    # Just go straight
    if (True):
        action = "moveStraight"


    print(action)
    takeAnAction()

    if (quarterLap == 4):
        quarterLap = 1
        lapCompleted = lapCompleted + 1

    wait(100)

#
