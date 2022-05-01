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
#pixy2 = Pixy2(port = 3, i2c_address = 0x54)
motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steering = Motor(Port.A, Direction.COUNTERCLOCKWISE)
#ir = InfraredSensor(Port.S4)
cs = ColorSensor(Port.S2)
gs = GyroSensor(Port.S1)
watch = StopWatch()



""" UTILS """

def getDistance():
    print("Distance:", ir.distance())
    return ir.distace()

def getColor():
    print("Color:", cs.color())
    return cs.color()

def getAngle():
    global quarterLap, k
    print("Angle:", gs.angle()-(quarterLap * 90 * k))
    return gs.angle() - (quarterLap * 90 * k)            #
    #return 90  -  (quarterLap * 90)

def goStraightOn():
    global steeringSpeed, lastCorrection, quarterLap
    if ( quarterLap == 0 or quarterLap == 2 or quarterLap == 3 or quarterLap == 1): ###
        correction = - lastCorrection - getAngle()
    elif ( quarterLap ):
        correction = - getAngle()

    lastCorrection = correction
    print("Correction:", correction)
    steering.run_angle(steeringSpeed, correction, wait = True)

def turnBlueLine():
    global steeringSpeed, flag_line, quarterLap
    flag_line = True
    steeringAngle = 40
    steering.run_angle(steeringSpeed, steeringAngle, wait = False) # Opening
    while (getAngle() < 88):
        wait(80)
    steering.run_angle(steeringSpeed, -steeringAngle, wait = True) # Closing
    quarterLap = quarterLap + 1

def turnOrangeLine():
    global steeringSpeed, flag_line, quarterLap
    flag_line = True
    steeringAngle = -40
    steering.run_angle(steeringSpeed, steeringAngle, wait = False) # Opening
    while (getAngle() > -88):
        wait(80)
    steering.run_angle(steeringSpeed, -steeringAngle, wait = True) # Closing
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
#motor.run(1000)

# Initializations
steeringSpeed = 150
motorSpeed = 1000
watch.reset()
gs.reset_angle(0)
flag_line = False
blocks = False
lastCorrection = 0
quarterLap = 0
lapCompleted = 0
action = ""
k = 1
# Ciclo equivalente al loop() di uno sketch Arduino
while True:

    # Acquiring information
    color = getColor()

    # Color Lines
    if (color == Color.RED):
        action = "onOrangeLine"
        k = -1
    elif (color == Color.BLUE):
        action = "onBlueLine"
        k = 1
    # Pixy
    elif (blocks):
        pass
    # Just go straight
    elif (True):
        action = "moveStraight"


    print(action)
    takeAnAction()
    print("Quarter Lap:", quarterLap)
    if (quarterLap == 3):
        quarterLap = 1
        lapCompleted = lapCompleted + 1

    wait(100)

#
