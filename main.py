#!/usr/bin/env pybricks-micropython
from pybricks.hubs       import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop
from pybricks.tools      import wait, StopWatch
from math                 import pi

# --- Inicialização do EV3 ---
EV3            = EV3Brick()
motorL         = Motor(Port.B)
motorR         = Motor(Port.C)
sensorL        = ColorSensor(Port.S1)
sensorR        = ColorSensor(Port.S2)
sensorA        = ColorSensor(Port.S3)
sensorB        = ColorSensor(Port.S4)
MOTOR_CENTRAL  = Motor(Port.A)

# --- Função de deslocamento ---
def andar_cm(distancia_cm, velocidade=200):
    diametro_roda = 4.8
    circunferencia = pi * diametro_roda
    rotacoes = distancia_cm / circunferencia
    angulo = rotacoes * 360

    motorL.reset_angle(0)
    motorR.reset_angle(0)
    motorL.run_angle(velocidade, angulo, wait=False)
    motorR.run_angle(velocidade, angulo, wait=True)
    motorL.hold()
    motorR.hold()

# --- Sua função de giro ---
def girar_graus(angulo, velocidade=200):
    MOTOR_CENTRAL.reset_angle(0)
    motorL.reset_angle(0)
    motorR.reset_angle(0)

    ang_abs = abs(angulo) * pi

    if angulo > 0:
        motorL.run_angle(velocidade,  ang_abs, wait=False)
        motorR.run_angle(velocidade, -ang_abs, wait=False)
        MOTOR_CENTRAL.run_angle(velocidade, ang_abs, wait=True)
    else:
        motorL.run_angle(velocidade, -ang_abs, wait=False)
        motorR.run_angle(velocidade,  ang_abs, wait=False)
        MOTOR_CENTRAL.run_angle(velocidade,  -ang_abs, wait=True)

    motorL.hold()
    motorR.hold()
    MOTOR_CENTRAL.hold()

# --- Seguidor de linha com PID ---
def seguir_linha_pid():
    Kp, Ki, Kd = 8, 0.5, 0.2
    base_speed = 150
    integral = 0
    last_error = 0

    while True:
        rL = sensorL.reflection()
        rR = sensorR.reflection()
        if rL is None or rR is None:
            EV3.speaker.beep()
            wait(200)
            continue

        # interrompe ao ver preto em S3 e S4
        if sensorA.reflection() < 38 and sensorB.reflection() < 15:
            motorL.stop()
            motorR.stop()
            return

        error = rL - rR
        integral = max(min(integral + error, 1000), -1000)
        deriv = error - last_error
        corr = Kp*error + Ki*integral + Kd*deriv
        last_error = error

        vL = max(min(base_speed - corr, 500), -500)
        vR = max(min(base_speed + corr, 500), -500)
        motorL.run(vL)
        motorR.run(vR)

        wait(20)

# --- Alinhamento de 2 segundos com thresholds separados e debug ---
def alinhar_linha():
    # agora você pode ajustar separadamente:
    THRESHOLD_A = 38   # limite para sensor A (porta S3)
    THRESHOLD_B = 13  # limite para sensor B (porta S4)
    SPEED = 100
    ANGLE_IN  = -15
    ANGLE_OUT = 15

    sw = StopWatch()
    sw.reset()
    print(">> Iniciando alinhamento (2 s)")
    while sw.time() < 2000:
        ra = sensorA.reflection()
        rb = sensorB.reflection()

        # debug no serial:
        print("  Sensor A:", ra, " vs TH_A:", THRESHOLD_A,
              " | Sensor B:", rb, " vs TH_B:", THRESHOLD_B)

        if ra is None or rb is None:
            EV3.speaker.beep()
            wait(200)
            continue

        # direito (sensorB)
        if rb < THRESHOLD_B:
            motorR.run_angle(SPEED, ANGLE_IN, then=Stop.HOLD, wait=True)
        else:
            motorR.run_angle(SPEED, ANGLE_OUT, then=Stop.HOLD, wait=True)

        motorR.stop()

        # esquerdo (sensorA)
        if ra < THRESHOLD_A:
            motorL.run_angle(SPEED, ANGLE_IN, then=Stop.HOLD, wait=True)
        else:
            motorL.run_angle(SPEED, ANGLE_OUT, then=Stop.HOLD, wait=True)

        motorL.stop()

        wait(50)

    print(">> Alinhamento concluído")

# --- Fluxo principal em loop infinito ---
def main():
    while True:
        seguir_linha_pid()
        alinhar_linha()
        andar_cm(5)
        girar_graus(-90, 700)
        EV3.speaker.beep()
        wait(500)

if __name__ == "__main__":
    main()
