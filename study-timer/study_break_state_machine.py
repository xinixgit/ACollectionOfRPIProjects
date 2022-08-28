from utime import sleep, ticks_ms, ticks_diff
from timer import count_down

class StudyBreakStateMachine:
    STUDY_STATE = 0
    STUDY_COMPLETE_STATE = 1
    BREAK_STATE = 2
    BREAK_COMPLETE_STATE = 3

    STUDY_DURATION_MS = 30 * 60 * 1000 # 30 min study
    BREAK_DURATION_MS = 5 * 60 * 1000 # 5 min break

    def __init__(self, buzzer, lcd_controller, state_start_callback):
        self.state = self.STUDY_STATE
        self.reset = False
        self.buzzer = buzzer
        self.lcd_controller = lcd_controller
        self.state_start_callback = state_start_callback

    def do_buzz(self):
        buzzer = self.buzzer
        while self.reset is False:
            for i in range(0, 4):
                if self.reset is True:
                    break
                for i in range(0, 4):
                    buzzer.duty_u16(40000)
                    sleep(0.1)
                    buzzer.duty_u16(0)
                    sleep(0.1)
                sleep(0.5)

            for i in range(0, self.BREAK_DURATION_MS / 1000):
                if self.reset is True:
                    break
                sleep(1)

    def next_state(self):
        self.state = (self.state + 1) % 4

    def reset_state(self):
        self.reset = True

    async def set_lcd_study(self, remain_in_sec):
        self.lcd_controller.set_study()
        self.lcd_controller.display_time(remain_in_sec)

    async def set_lcd_break(self, remain_in_sec):
        self.lcd_controller.set_break()
        self.lcd_controller.display_time(remain_in_sec)

    def run(self):
        state = self.state
        self.state_start_callback(state)

        if state == self.STUDY_STATE:
            count_down(self.STUDY_DURATION_MS, lambda: self.reset, [self.set_lcd_study])
        elif state == self.BREAK_STATE:
            count_down(self.BREAK_DURATION_MS, lambda: self.reset, [self.set_lcd_break])
        elif state in (self.STUDY_COMPLETE_STATE, self.BREAK_COMPLETE_STATE):
            self.do_buzz()
        else:
            raise ValueError('State {state} is not valid'.format(state = state))

        self.next_state()
        self.reset = False
