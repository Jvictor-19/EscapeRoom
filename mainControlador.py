from  machine import Pin
import utime
import sys

# Definição dos pinos do motor
pin_a = Pin(0, Pin.OUT)
pin_b = Pin(1, Pin.OUT)
pin_c = Pin(2, Pin.OUT)
pin_d = Pin(3, Pin.OUT)

def motor_off():
    pin_a.low()
    pin_b.low()
    pin_c.low()
    pin_d.low()

def motor_sequence(steps=1000, delay=0.002):
    for _ in range(steps):
        pin_a.high(); pin_b.low();  pin_c.low();  pin_d.high()
        utime.sleep(delay)

        pin_a.high(); pin_b.high(); pin_c.low();  pin_d.low()
        utime.sleep(delay)

        pin_a.low();  pin_b.high(); pin_c.high(); pin_d.low()
        utime.sleep(delay)

        pin_a.low();  pin_b.low();  pin_c.high(); pin_d.high()
        utime.sleep(delay)

    motor_off()

motor_off()
print("Pronto para receber comandos pela serial")

# Loop principal ouvindo a serial
while True:
    cmd = sys.stdin.readline().strip()
    if cmd == "ACTIVATE_MOTOR":
        print("Recebido: ativar motor")
        motor_sequence(500)   # roda 500 passos
    elif cmd == "STOP":
        print("Motor parado")
        motor_off()
