from utime import sleep

def ring_buzz(buzzer, duty_u16, should_stop):    
    while True:
        for i in range(0, 4):
            buzzer.duty_u16(duty_u16)
            sleep(0.1)
            buzzer.duty_u16(0)
            sleep(0.1)
            
        if should_stop():
            return
        
        sleep(0.5)


