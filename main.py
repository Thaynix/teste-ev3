#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import pi

ev3 = EV3Brick()

#-- Motores
motorC = Motor(Port.A) # motor para giro 
motorL = Motor(Port.B) # motor esquerdo
motorR = Motor(Port.C) # motor direito

#motorG = Motor(Port.D) # motor braço da garra 
motorG2 = Motor(Port.D) # motor da garra

#-- Sensores

# sensorCorR = ColorSensor(Port.S1) # sensor do lado direito inferior
# sensorCorL = ColorSensor(Port.S2) # sensor do lado esquerdo inferior

# sensor da garra direita
sensorUltraR = UltrasonicSensor(Port.S1)
# sensorUltraL = UltrasonicSensor(Port.S4)
# SensorUltrassom = UltrasonicSensor(Port.S3)

# controle dos motor
ganho = 2.0
ref = 20
potencia = 100
potencia_min = 50   
potencia_max = 200

# Função seguir linha
# def seguir_linha():
#     while True:
#         refL = sensorCorL.reflection()
#         refR = sensorCorR.reflection()

#         if refL is None or refR is None:
#             ev3.speaker.beep()
#             continue

#         print("Reflexão Esquerdo: " + str(refL))
#         print("Reflexão Direito:" + str(refR))

#         if refL > 20 and refR > 20:
#             motorL.run(potencia_max)
#             motorR.run(potencia_max)
#             motorC.stop()
        
#         if refL < 8:
#             motorL.run(-potencia_max)
#             motorR.run(potencia_max)
#             motorC.run(potencia_max)
        
#         if refR < 8:
#             motorL.run(potencia_max)
#             motorR.run(-potencia_max)
#             motorC.run(-potencia_max)

# seguir_linha()

def mover_garra():
    distR = sensorUltraR.distance() / 10
    
    while True:
        print(sensorUltraR.distance()/10)
    
        if distR < 10:
            motorG2.run(-potencia_max)
        if distR > 10:
            motorG2.run(potencia_max)
        # if distR == 8:
        #     motorG.stop

mover_garra()

# def abre_fecha_garra():
#     # motorG2.reset_angle(0)  # Define a posição atual como 0 (fechado)

#     while True:
#         distR = sensorUltraR.distance() / 10  # Lê a distância em cm

#         if distR < 6:
#             # Fecha a garra (vai até 0°)
#             # motorG2.run_angle(500, 0)
        
#         elif distR > 7:
#             # Abre a garra (vai até 90°)
#             # motorG2.run_angle(500, 90)

#         wait(200)

# abre_fecha_garra()