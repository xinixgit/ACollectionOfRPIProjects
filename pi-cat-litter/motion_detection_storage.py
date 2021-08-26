from datetime import datetime
import paho.mqtt.client as mqtt
import mariadb
import sys
import json
import argparse

TOPIC = 'Home/Sensor/Motion_Detection_Event'

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--db-username', required=True)
parser.add_argument('-p', '--db-password', required=True)
parser.add_argument('-d', '--database', required=True)

args, unknown = parser.parse_known_args()

def printMessage(msg):
	print(f"{str(datetime.now())} - " + msg)

# Establish a database connection
try:
	conn = mariadb.connect(
		user=args.db_username,
		password=args.db_password,
		host="localhost",
		port=3306,
		database=args.database

	)
	cur = conn.cursor()
	printMessage('Connected with database')
except mariadb.Error as e:
	printMessage(f"error connecting to MariaDB Platform: {e}")
	sys.exit(1)

def log_db(obj):
	try:
		cur.execute(
			"INSERT INTO motion_detection (detector_name, detection_time_epoch, detection_time) VALUES (?, ?, ?)",
			(obj['detector_name'], obj['detection_time_epoch'], obj['detection_time_str']))
		conn.commit()
		printMessage(f"inserted id: {cur.lastrowid}")
	except mariadb.Error as e:
		printMessage(f"error: {e}")

def on_connect(client, userdata, flags, rc):
  printMessage("Connected to MQTT broker with result code "+str(rc))
  client.subscribe(TOPIC)

def on_message(client, userdata, msg):
	json_obj = json.loads(msg.payload.decode('utf-8'))
	log_db(json_obj)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set('/etc/mosquitto/ca_certificates/ca.crt', '/home/pi/ssl/client.crt', '/home/pi/ssl/client.key')
client.connect("pz-cat-litter", 8883, 60)
client.loop_forever()
