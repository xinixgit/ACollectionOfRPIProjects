from threading import Thread
import paho.mqtt.client as mqtt
import json

MQTT_HOST = "10.12.0.188"


def on_connect(client, userdata, flags, rc):
    print("event broker connected with result code "+str(rc))
    # client.subscribe("/feederv2/camera")


def on_message(client, userdata, msg):
    json_str = msg.payload.decode('utf8').replace("'", '"')
    map = json.loads(json_str)
    print('received', json_str, 'from', msg.topic)

    if msg.topic == '/feeder/random':
        pass


class EventListener:
    def __init__(self):
        userdata = {}
        self.client = mqtt.Client(userdata=userdata)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def connect(self, user='', pwd=''):
        self.client.username_pw_set(user, pwd)
        self.client.connect(host=MQTT_HOST, port=1883, keepalive=30)
        thread = Thread(target=self.client.loop_forever)
        thread.start()
        print("event listener started")

    def disconnect(self):
        self.client.disconnect()

    def publish_portion_fed(self, portion_fed: int):
        self.client.publish('/feeder/event/portion_fed', portion_fed)
