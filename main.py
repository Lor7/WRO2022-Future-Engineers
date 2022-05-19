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
    return ir.distance()

def getColor():
    print("Color:", cs.color())
    return cs.color()

def getAngle():
    global quarterLap, k, anglePosOrNeg
    angle = gs.angle()
    if (angle < 0):
        anglePosOrNeg = -1
    else:
        anglePosOrNeg = 1
    print("Angle:",  angle - (quarterLap * 90 * k))
    
    # return abs(angle) % 90 * anglePosOrNeg
    return angle - (quarterLap * 90 * k)          
    # return 90  -  (quarterLap * 90)

def goStraightOn():
    global steeringSpeed, correction, lastCorrection

    steering.run_angle(steeringSpeed, -lastCorrection, wait = True)
    correction = -getAngle()
    print("Correction: {correction}".format(correction = correction))
    steering.run_angle(steeringSpeed, correction, wait = True)
    lastCorrection = correction


def turnBlueLine():
    global steeringSpeed, flag_line, quarterLap, lastCorrection
    flag_line = True
    steeringAngle = 55
    steering.run_angle(steeringSpeed, steeringAngle - lastCorrection, wait = False) # Opening
    lastCorrection = 0
    while (getAngle() < 85):
        wait(20)
    steering.run_angle(steeringSpeed, -steeringAngle, wait = True) # Closing
    quarterLap = quarterLap + 1

def turnOrangeLine():
    global steeringSpeed, flag_line, quarterLap, lastCorrection
    flag_line = True
    steeringAngle = -55
    steering.run_angle(steeringSpeed, steeringAngle - lastCorrection, wait = False) # Opening
    lastCorrection = 0
    while (getAngle() > -85): # - 95
        wait(20)
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


def moveToBlock(X, Y, W, H, Angle, typeC):
    global focalLengthWidth, focalLengthHeight
    focalLengthWidth = (calWidth * calDistance) / 10
    focalLengthHeight = (calHeight * calDistance) / 25

    distanceWidth = (W * focalLengthWidth) / W
    distanceHeight = (H * focalLengthHeight) / H

    distanceIR1 = ir.distance()
    distanceIR2 = ir2.distance()


    if (typeC == "G"):

        
        if (distanceIR1 > distanceIR2):
            angleToBLock =  getSteeringAngle(X + (distanceIR1 / distanceIR2 * 12))
        else: 
            angleToBLock = getSteeringAngle(X - (distanceIR2 / distanceIR1 * 12))
        steering.run_angle(25, angleToBlock)    
        wait(80)
        angleToBlock2 = getSteeringAngle(X)
        steering.run_angle(25, (angleToBlock - angleToBlock2))   
    else:
        if (distanceIR2 > distanceIR1):
            angleToBLock = getSteeringAngle(X - (distanceIR2 / distanceIR1 * 12))
        else: 
            angleToBLock = getSteeringAngle(X + (distanceIR1 / distanceIR2 * 12))
        steering.run_angle(25, angleToBlock)    
        wait(80)
        angleToBlock2 = getSteeringAngle(X)
        steering.run_angle(25, (angleToBlock - angleToBlock2))    

def getSteeringAngle(X):
    angle = (126.5 - X) / 2.611
    return angle 


def resetSteeringAngle():
    steering.reset_angle(0)



""" ALGORITHM """

# Avvio la propulsione
motor.run(1000)

# Initializations
steeringSpeed = 150
motorSpeed = 1000
watch.reset()
gs.reset_angle(0)
flag_line = False
blocks = False
quarterLap = 0
lapCompleted = 0
action = ""
anglePosOrNeg = 1
k = 1
correction = 0
lastCorrection = 0
time = 0
nextTimeToCorrection = 0
realBlockWidth = 10
realBlockHigh = 20
calWidth = 40
calHeight = 29
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
    nr_blocks, block = pixy2.get_blocks(1, 1)
    if (nr_blocks > 0):

        sig = block[0].sig
        redX = block[0].x_center
        redY = block[0].y_center
        redW = block[0].width
        redH = block[0].height
        redAngle = blocks[0].angle

    nr_blocks, block = pixy2.get_blocks(2, 1)
    if (nr_blocks > 0):
        sig = block[0].sig
        greenX = block[0].x_center
        greenY = block[0].y_center
        greenW = block[0].width
        greenH = block[0].height
        greenAngle = blocks[0].angle
    elif (blocks):
        if (greeH > redH):
            moveToBlock(greenX, greenY, greenW, greenH, 50, "G")
        else:
            moveToBlock(redX, redY, redW, redH, -50, "R")
    # Just go straight
    elif (True):
        action = "moveStraight"


    print(action)
    takeAnAction()

    if (quarterLap % 3 == 0 and flag_line == True):
        print("Lap {lapCompleted} completed!".format(lapCompleted = lapCompleted))
        lapCompleted = lapCompleted + 1
        flag_line = False
        if (lapCompleted == 3):
            break
    
    wait(100)

motor.run_time(1000, 10000, wait = False)
secondsBeforeStopRobot = watch.time()
while secondsBeforeStopRobot < watch.time() + 9500:
    goStraightOn()
    wait(400)
    
