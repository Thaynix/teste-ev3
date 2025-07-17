#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

# Inicialização do EV3 e dos dispositivos
ev3 = EV3Brick()
motorL = Motor(Port.B)
motorR = Motor(Port.C)
sensorL = ColorSensor(Port.S1)
sensorR = ColorSensor(Port.S2)

# Parâmetros PID
Kp = 10     # ganho proporcional
Ki = 0.5    # ganho integral
Kd = 0.2     # ganho derivativo

# Velocidade de base
base_speed = 150

# Limites para o termo integral (anti-windup)
integral_min = -1000
integral_max =  1000

# Variáveis de estado do PID
integral = 0
last_error = 0

# Função principal
def seguir_linha_pid():
    global integral, last_error
    
    while True:
        # 1) Leitura das reflexões
        reflL = sensorL.reflection()
        reflR = sensorR.reflection()
        
        # Se alguma leitura falhar, sinal audível e pula
        if reflL is None or reflR is None:
            ev3.speaker.beep()
            wait(200)
            continue
        
        # 2) Cálculo do erro
        #    Se a linha for preta sobre fundo claro: linha → valor baixo
        #    Erro = (valor do sensor esquerdo) - (valor do sensor direito)
        error = reflL - reflR
        
        # 3) Termo integral
        integral += error
        # Anti-windup
        if integral > integral_max:
            integral = integral_max
        elif integral < integral_min:
            integral = integral_min
        
        # 4) Termo derivativo
        derivative = error - last_error
        
        # 5) Sinal de correção
        correction = Kp * error + Ki * integral + Kd * derivative
        
        # 6) Ajuste das velocidades dos motores
        #    Para virar para o lado certo, subtrai ou adiciona ao base_speed
        left_speed  = base_speed - correction
        right_speed = base_speed + correction
        
        # 7) Limita velocidades ao permitido pelo motor
        left_speed  = max(min(left_speed,  500), -500)
        right_speed = max(min(right_speed, 500), -500)
        
        # 8) Executa motores
        motorL.run(left_speed)
        motorR.run(right_speed)
        
        # 9) Atualiza estado
        last_error = error
        
        # Pequena pausa para estabilidade de loop
        wait(20)

# Executa o seguidor de linha com PID
seguir_linha_pid()
