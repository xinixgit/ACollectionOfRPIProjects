from machine import Pin, PWM
from study_break_state_machine import StudyBreakStateMachine
from lcd_controller import LcdController

reset_button = Pin(28, Pin.IN, Pin.PULL_DOWN)

grnled = Pin(22, Pin.OUT)
redled = PWM(Pin(21))
redled.freq(1000)

buzzer = PWM(Pin(16))
buzzer.freq(2000)

lcd_controller = LcdController()

def state_start_callback(state):
    if state == StudyBreakStateMachine.STUDY_STATE:
        grnled.value(0)
        redled.duty_u16(10000)
    elif state == StudyBreakStateMachine.BREAK_STATE:
        redled.duty_u16(0)
        grnled.value(1)
    lcd_controller.display_time(0)

state_machine = StudyBreakStateMachine(buzzer, lcd_controller, state_start_callback)

def reset_state(pin):
    global state_machine
    state_machine.reset_state()

reset_button.irq(reset_state, Pin.IRQ_FALLING)

while True:
    state_machine.run()
