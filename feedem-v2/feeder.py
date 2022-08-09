from gpiozero import Button, LED

class Feeder:
    def __init__(self):
        self.detect = Button(23)
        self.feed_trigger = LED(25)
        self.button = Button(24)
        self.button.when_pressed = self.on_user_button_pressed

    def feed(self, portion: int) -> None:
        if not self.feed_trigger.is_lit:
            self.feed_trigger.on()
            while portion > 1:
                print("now feeding 1 portion")
                self.detect.wait_for_press()
                portion-=1
            self.feed_trigger.off()

    def on_user_button_pressed(self) -> None:
        self.feed(1)