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
        self.last_ts = ''
        self.last_ts_unit = ''
        # init lcd
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr('Mode:    ')
        self.lcd.move_to(0, 1)
        self.lcd.putstr('Remain:  ')

    def refresh_state(self):
        lcd = self.lcd
        lcd.move_to(9, 0)
        lcd.putstr(self.state)

    def set_study(self):
        self.state = 'Study'
        self.refresh_state()

    def set_break(self):
        self.state = 'Break'
        self.refresh_state()

    def get_time_str(self, ts):
        if ts <= 0:
            return ('00', 'sec')

        min = int(ts / 60)
        sec = int(ts % 60)
        if min >= 10: # at least 10 min
            return (str(min), 'min')
        elif min >= 1:  # at least 1 min
            return ('0' + str(min), 'min')
        elif ts >= 10:  # more than 10 sec
            return (str(ts), 'sec')
        else:
            return ('0' + str(ts), 'sec')

    def display_time(self, time_remain_sec):
        ts, unit = self.get_time_str(time_remain_sec)
        if self.last_ts == ts and self.last_ts_unit == unit:
            return

        lcd = self.lcd
        if self.last_ts != ts:
            lcd.move_to(9, 1)
            lcd.putstr(ts)
            self.last_ts = ts

        if self.last_ts_unit != unit:
            lcd.move_to(12, 1)
            lcd.putstr(unit)
            self.last_ts_unit = unit
