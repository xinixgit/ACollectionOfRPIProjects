import paho.mqtt.client as mqtt
import sys
import time
import json
from gpiozero import MotionSensor, LED
from datetime import datetime
from signal import pause

outpin = LED(22)
pir = MotionSensor(27, sample_rate=1)

FAN_ON_DURATION = 30 * 60		# 30 min

TOPIC = 'Home/Sensor/Motion_Detection_Event'

ts_prev_triggered = 0

def printMessage(msg):
	print(f"{str(datetime.now())} - " + msg)

printMessage("Motion detection init...")

def publish_mqtt():
	global client
	epoch = int(time.time())
	time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
	payload = {}
	payload['detector_name'] = 'pz-cat-litter'
	payload['detection_time_epoch'] = epoch
	payload['detection_time_str'] = time_str
	json_obj = json.dumps(payload)
	infot = client.publish(TOPIC, json_obj)
	printMessage(f'message {json_obj} published: {infot}')

def on_connect(client, userdata, flags, rc):
  printMessage("Connected to MQTT broker with result code "+str(rc))

def activate_fan():
	outpin.on()
	printMessage("fan activated.")
	time.sleep(FAN_ON_DURATION)
	outpin.off()
	printMessage("fan de-activated")

def on_motion_detected():
  global ts_prev_triggered
  now = datetime.now()
  # prevent the sensor from getting triggered accidentally
  if (ts_prev_triggered == 0 or int((now - ts_prev_triggered).total_seconds()) > 15):
      printMessage(f"motion has been triggered more than 15s ago at {ts_prev_triggered}")
      ts_prev_triggered = now
      time.sleep(5)
      return
  ts_prev_triggered = 0
  publish_mqtt()
  activate_fan()

printMessage("Motion detection ready...")

client = mqtt.Client()
client.on_connect = on_connect

client.tls_set('/etc/mosquitto/ca_certificates/ca.crt', '/home/pi/ssl/client.crt', '/home/pi/ssl/client.key')
client.connect("pz-cat-litter", 8883, 60)
client.loop_start()

while True:
	pir.wait_for_motion()
	on_motion_detected()
