from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import time

pir = MotionSensor(14)
camera = PiCamera()

# Set up the camera
camera.resolution = (1600, 1200)

CAPTURE_GAP = 10  # wait at least 10 sec before taking pictures

def capture():
  timestamp = datetime.now().isoformat()
  fname = ('/home/pi/images/%s.jpg' % timestamp).replace(':', '.')
  camera.capture(fname)

while True:
  pir.wait_for_motion()
  capture()
  time.sleep(CAPTURE_GAP)
