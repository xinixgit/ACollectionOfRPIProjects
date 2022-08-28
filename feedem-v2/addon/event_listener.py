from threading import Thread
from .cam_streamer import CamStreamer
import paho.mqtt.client as mqtt
import json

MQTT_HOST = "192.168.0.181"

def on_connect(client, userdata, flags, rc):
    print("event broker connected with result code "+str(rc))
    client.subscribe("/feederv2/camera")

def on_message(client, userdata, msg):
    json_str = msg.payload.decode('utf8').replace("'", '"')
    map = json.loads(json_str)
    print('received', json_str, 'from', msg.topic)

    if msg.topic == '/feederv2/camera':
        if map['action'] == 'start':
            userdata['cam'].start_recording()
        elif map['action'] == 'stop':
            userdata['cam'].stop_recording()

class EventListener:
    def __init__(self, cam: CamStreamer):  
        userdata = {
            'cam': cam
        }
        self.client = mqtt.Client(userdata=userdata)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def connect(self):
        self.client.connect(MQTT_HOST, 1883, 60)
        thread = Thread(target=self.client.loop_forever)
        thread.start()
        print("event listener started")

    def disconnect(self):
        self.client.disconnect()
