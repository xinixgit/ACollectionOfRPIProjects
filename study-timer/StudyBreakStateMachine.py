from utime import sleep, ticks_ms, ticks_diff
from lcd_controller import LcdController

class StudyBreakStateMachine:    
    STUDY_STATE = 0
    STUDY_COMPLETE_STATE = 1
    BREAK_STATE = 2
    BREAK_COMPLETE_STATE = 3
    
    STUDY_DURATION_MS = 30 * 60 * 1000 # 30 min study
    BREAK_DURATION_MS = 5 * 60 * 1000 # 5 min break
    
    def __init__(self, buzzer, state_start_callback):
        self.state = self.STUDY_STATE
        self.reset = False
        self.buzzer = buzzer
        self.state_start_callback = state_start_callback
        self.lcd_controller = LcdController()
        
    def do_buzz(self):
        buzzer = self.buzzer
        while self.reset is False:
            for i in range(0, 4):
                buzzer.duty_u16(40000)
                sleep(0.1)
                buzzer.duty_u16(0)
                sleep(0.1)
            sleep(0.5)
            
    def do_sleep(self, duration_ms):
        ts_start = ticks_ms()
        while self.reset is False:
            ts_diff = ticks_diff(ticks_ms(), ts_start)
            if ts_diff >= duration_ms:
                break
            
            self.lcd_controller.set_time_elapsed(int(ts_diff / 1000))
            self.lcd_controller.refresh_screen()
            sleep(1)
            
    def next_state(self):
        self.state = (self.state + 1) % 4
        
    def reset_state(self):
        self.reset = True
        
    def run(self):
        state = self.state
        lcd_controller = self.lcd_controller
        self.state_start_callback(state)
        
        if state == self.STUDY_STATE:
            lcd_controller.set_study()
            self.do_sleep(self.STUDY_DURATION_MS)
        elif state == self.BREAK_STATE:
            lcd_controller.set_break()
            self.do_sleep(self.BREAK_DURATION_MS)
        elif state in (self.STUDY_COMPLETE_STATE, self.BREAK_COMPLETE_STATE):
            self.do_buzz()
        else:
            raise ValueError('State {state} is not valid'.format(state = state))
        
        self.next_state()
        self.reset = False

