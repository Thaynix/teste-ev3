#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.    


# Create your objects here.
ev3 = EV3Brick()

motor = Motor(Port.B)
sencor = ColorSensor(Port.S1)

def sensorCor():
    while True:
        sensorcor = sencor.color()
    
        print("cor: ", sensorcor)
        wait(1000)

def rotmotor():
    while True:
        print(sencor.color())
        while sencor.color() == Color.BLACK:
            motor.run(500)
            wait(1000)
        motor.run(0)
        ev3.speaker.beep(frequency=1000, duration=500)

rotmotor()
# sensorCor()
# motor.run(1000)      
# wait(5000)
ev3.speaker.beep()


# test_motor.run_target(1000, 90)

ev3.speaker.beep(frequency=1000, duration=500)