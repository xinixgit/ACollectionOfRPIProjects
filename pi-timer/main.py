from machine import Pin, PWM
from utime import sleep, ticks_ms
from buzzer import ring_buzz

RED_LED_DUTY_ON = 10000
BUZZER_DUTY_ON = 40000 # how loud the buzz should sound

STUDY_DURATION_MS = 30 * 60 * 1000 # 30 min study
BREAK_DURATION_MS = 5 * 60 * 1000 # 5 min break

reset = False
reset_button = Pin(28, Pin.IN, Pin.PULL_DOWN)

grnled = Pin(22, Pin.OUT)
redled = PWM(Pin(21))
redled.freq(1000)

buzzer = PWM(Pin(16))
buzzer.freq(2000)

def buzz():
    global buzzer, reset
    ring_buzz(buzzer, BUZZER_DUTY_ON, lambda: reset)
    reset = False

def reset_state(pin):
    global reset
    reset = True
    
reset_button.irq(reset_state, Pin.IRQ_FALLING) # interrupt the buzz and go into the next state

def resettable_sleep(duration):
    global reset
    ts_start = ticks_ms()
    while reset is False and (ticks_ms() - ts_start) < duration:
        sleep(1)
    reset = False

def do_study():
    redled.duty_u16(RED_LED_DUTY_ON)
    resettable_sleep(STUDY_DURATION_MS)
    buzz()
    redled.duty_u16(0)
    
def do_break():
    grnled.value(1)
    resettable_sleep(BREAK_DURATION_MS)
    buzz()
    grnled.value(0)    

while True:
    do_study()
    do_break()

