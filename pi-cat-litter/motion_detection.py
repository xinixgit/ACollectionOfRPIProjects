import mariadb
import sys
import time
from gpiozero import MotionSensor, LED
from datetime import datetime
from signal import pause

outpin = LED(22)
pir = MotionSensor(27, sample_rate=1)

FAN_ON_DURATION = 10 * 60		# 10 min

def printMessage(msg):
	print(f"{str(datetime.now())} - " + msg)

printMessage("Motion detection init...")

def runfan():
	outpin.on()
	printMessage("fan activated.")
	time.sleep(FAN_ON_DURATION)
	outpin.off()
	printMessage("fan de-activated")

#
def logdb():
	epoch = int(time.time())
	time_h = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
	try:
		cur.execute(
			"INSERT INTO motion_detection (detector_name, detection_time_epoch, detection_time) VALUES (?, ?, ?)",
			('pz-cat-litter', epoch, time_h))
		conn.commit()
		printMessage(f"inserted id: {cur.lastrowid}")
	except mariadb.Error as e:
		printMessage(f"error: {e}")


def on_motion_detected():
	logdb()
	runfan()


# Establish a connection
try:
  conn = mariadb.connect(
      user=username,
      password=password,
      host="localhost",
      port=3306,
      database="exports"

  )
  cur = conn.cursor()
except mariadb.Error as e:
  printMessage(f"error connecting to MariaDB Platform: {e}")
  sys.exit(1)

printMessage("motion detection ready...")

while True:
	pir.wait_for_motion()
	on_motion_detected()
