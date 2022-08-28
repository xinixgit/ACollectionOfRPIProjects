from gpiozero import Button, LED
import time

class Feeder:
    def __init__(self):
        self.detect_button = Button(23) # detect signal from machine to know 1 portion has been fed
        self.detect_button.when_pressed = self.on_detect_button_pressed
        
        self.feed_button = Button(24) # feed 1 portion when pressed
        self.feed_button.when_pressed = self.on_feed_button_pressed

        self.feed_trigger = LED(25) # delivers a feed signal to transistor when activated

    def feed(self, portion: int) -> None:
        print("feeding {0} portions started".format(portion))
        just_pressed = False
        if not self.feed_trigger.is_lit:
            self.feed_trigger.on()
            while True:
                while self.detect_button.is_pressed:
                    if not just_pressed:
                        if portion == 0:
                            self.feed_trigger.off()
                            print("feeding completed")
                            return

                        print("feeding 1 portion") 
                        portion -= 1
                        just_pressed = True

                just_pressed = False
                time.sleep(0.1)
        

    def on_feed_button_pressed(self) -> None:
        print("adhoc feed button pressed")
        self.feed(1)

    def on_detect_button_pressed(self) -> None:
        print("detect button pressed")