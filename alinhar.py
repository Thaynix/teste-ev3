#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

# Inicialização
ev3     = EV3Brick()
motorL  = Motor(Port.B)
motorR  = Motor(Port.C)
sensorL = ColorSensor(Port.S3)
sensorR = ColorSensor(Port.S4)

# Parâmetros
THRESHOLD    = 10    # Reflexão abaixo disso é preto
ADJUST_SPEED = 100   # Velocidade de ajuste
ADJUST_ANGLE = -15   # Gira para “aproximar” do preto
ANGLE        = 15    # Gira para “afastar” do preto

def alinhar_linha():
    while True:
        refL = sensorL.reflection()
        refR = sensorR.reflection()

        if refL is None or refR is None:
            ev3.speaker.beep()
            wait(200)
            continue

        # --- Lado Direito ---
        if refR < THRESHOLD:
            # Se vê preto: faz um único ajuste e para o motor
            motorR.run_angle(ADJUST_SPEED, ADJUST_ANGLE, then=Stop.HOLD, wait=True)
            motorR.stop()                    # garante parada completa
        else:
            # Se vê claro: faz um único ajuste e para o motor
            motorR.run_angle(ADJUST_SPEED, ANGLE, then=Stop.HOLD, wait=True)
            motorR.stop()

        # --- Lado Esquerdo ---
        if refL < THRESHOLD:
            motorL.run_angle(ADJUST_SPEED, ADJUST_ANGLE, then=Stop.HOLD, wait=True)
            motorL.stop()
        else:
            motorL.run_angle(ADJUST_SPEED, ANGLE, then=Stop.HOLD, wait=True)
            motorL.stop()

        # Pequena pausa antes da próxima leitura
        wait(10)

# Inicia o processo
alinhar_linha()
