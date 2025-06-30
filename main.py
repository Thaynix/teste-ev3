#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Inicia o EV3
ev3 = EV3Brick()

# Motores
motorL = Motor(Port.B)
motorR = Motor(Port.C)
# motorCentral = Motor(Port.A)

# Sensores
sensorCorR = ColorSensor(Port.S1)
sensorCorL = ColorSensor(Port.S2)


# Função andar
def andar():
    while True:
        potenciaL = 50
        potenciaR = 50
        motorR.run(potenciaR)
        motorL.run(potenciaL)
        wait(1000)  

# Função para sensor de cor
def sensorCor():
    while True:
        sensorR = sensorCorR.color()
        sensorL = sensorCorL.color()
        if sensorL and sensorR == Color.BROWN:
            andar()
        else:
            andar.stop()
        wait(1000)
sensorCor()

wait(2000)
