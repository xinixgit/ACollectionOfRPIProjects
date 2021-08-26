import utime

import machine
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
        self.last_min_str = None
        
    def set_study(self):
        self.state = 'Study'
        
    def set_break(self):
        self.state = 'Break'
        
    def set_time_elapsed(self, time_in_sec):
        self.time_in_sec = time_in_sec
        
    def get_str(self, ts):
        if ts == 0:
            return '00'
        elif ts >= 10:
            return str(ts)
        else:
            return '0' + str(ts)
        
    def refresh_screen(self):        
        time_in_sec = self.time_in_sec
        min = int(time_in_sec / 60)
        min_str = self.get_str(min)
        
        if self.last_min_str == min_str:
            return
        
        lcd = self.lcd
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Mode:   ' + self.state)
        
        min = int(time_in_sec / 60)        
        lcd.move_to(0, 1)
        lcd.putstr('Time:   ' + min_str + ' min')
        
        self.last_min_str = min_str
        


