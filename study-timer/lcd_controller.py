import utime
import machine

from utime import sleep, ticks_ms
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

class LcdController:
    def __init__(self):
        i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
        self.lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
        self.t_start_ms = 0
        self.t_total_ms = 0
        self.last_min_str = ''
        # init lcd
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr('Mode:    ')
        self.lcd.move_to(0, 1)
        self.lcd.putstr('Remain:  ')

    def set_study(self):
        self.state = 'Study'

    def set_break(self):
        self.state = 'Break'

    def get_str(self, ts):
        if ts <= 0:
            return '00 sec'

        min = int(ts / 60)
        sec = int(ts % 60)
        if min >= 10: # at least 10 min
            return str(min) + ' min'
        elif min >= 1:  # at least 1 min
            return '0' + str(min) + ' min'
        elif ts >= 10:  # more than 10 sec
            return str(int(sec / 10) * 10) + ' sec'
        elif ts >= 5:
            return '05 sec'
        else:
            return '0' + str(ts) + ' sec'

    def display_time(self, time_remain_sec):
        min_str = self.get_str(time_remain_sec)
        if self.last_min_str == min_str:
            return

        lcd = self.lcd
        lcd.move_to(9, 0)
        lcd.putstr(self.state)
        lcd.move_to(9, 1)
        lcd.putstr(min_str)

        self.last_min_str = min_str
