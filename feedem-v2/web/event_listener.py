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
    def __init__(self, user='', pwd=''):
        userdata = {}
        self.client = mqtt.Client(userdata=userdata)
        self.client.username_pw_set(user, pwd)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def __connect(self):
        self.client.connect(host=MQTT_HOST, port=1883)

    def __disconnect(self):
        self.client.disconnect()

    def publish_portion_fed(self, portion_fed: int):
        """
        Since the event is not frequent, we don't have to maintain a connection that is often
        disconnected. We establish connection right before publish.
        """
        try:
            self.__connect()
            self.client.publish('/feeder/event/portion_fed', portion_fed)
            self.__disconnect()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            print("failed to publish portion fed via MQTT.")
