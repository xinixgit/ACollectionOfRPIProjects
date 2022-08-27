from threading import Thread
import paho.mqtt.client as mqtt
import json
import time

MQTT_HOST = "192.168.0.181"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/feederv2/camera")

def on_message(client, userdata, msg):
    json_str = msg.payload.decode('utf8').replace("'", '"')
    map = json.loads(json_str)
    if msg.topic == '/feederv2/camera':
        if map['action'] == 'start':
            userdata['on_cam_start_event']()


class EventListener:
    def __init__(self, on_cam_start_event):  
        fn_map = {
            'on_cam_start_event': on_cam_start_event
        }
        self.client = mqtt.Client(userdata=fn_map)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def connect(self):
        self.client.connect(MQTT_HOST, 1883, 60)
        thread = Thread(target=self.client.loop_forever)
        thread.start()

    def disconnect(self):
        self.client.disconnect()
