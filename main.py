#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import pi


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Motores
motorC = Motor(Port.A)
motorL = Motor(Port.B)
motorR = Motor(Port.C)

# Motores da garra
motorG = Motor(Port.D)
motorG2 = Motor(Port.D)
# Sensores
sensorCorR = ColorSensor(Port.S1)
sensorCorL = ColorSensor(Port.S2)

# sensor da garra direita
sensorUltraR = UltrasonicSensor(Port.S3)
sensorUltraL = UltrasonicSensor(Port.S4)
# SensorUltrassom = UltrasonicSensor(Port.S3)

# controle dos motor
ganho = 2.0
ref = 20
potencia = 100
potencia_min = 50   
potencia_max = 200

# Função seguir linha
def seguir_linha():
    while True:
        refL = sensorCorL.reflection()
        refR = sensorCorR.reflection()

        if refL is None or refR is None:
            ev3.speaker.beep()
            continue

        print("Reflexão Esquerdo: " + str(refL))
        print("Reflexão Direito:" + str(refR))

        if refL > 20 and refR > 20:
            motorL.run(potencia_max)
            motorR.run(potencia_max)
            motorC.stop()
        
        if refL < 8:
            motorL.run(-potencia_max)
            motorR.run(potencia_max)
            motorC.run(potencia_max)
        
        if refR < 8:
            motorL.run(potencia_max)
            motorR.run(-potencia_max)
            motorC.run(-potencia_max)

seguir_linha()

def mover_garra():
    distR = sensorUltraR.distance() / 10
    distL = sensorUltraL.distance() / 10
    mediaDist = distR + distL / 2

    while True:
        print(sensorUltraR.distance)
    
        if mediaDist < 7:
            motorG.run_target(-potencia, 90)
        if distR > 7:
            motorG.run(potencia, -90)

mover_garra()

def abre_fecha_garra():
    motorG2.reset_angle(0) 

    while True:
        distR = sensorUltraR.distance() / 10  

        if distR < 6:
            # Fecha a garra (vai até 0°)
            motorG2.run_angle(500, 0)
        
        elif distR > 7:
            # Abre a garra (vai até 90°)
            motorG2.run_angle(500, 90)

        wait(200)

# abre_fecha_garra()