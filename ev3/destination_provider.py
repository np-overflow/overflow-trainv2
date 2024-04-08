# import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

# The hostname or IP address of the remote broker
HOST = "192.168.0.69"

class DestinationProvider:
    def __init__(self):
        pass

    def get_next_destination(self):
        msg = subscribe.simple("bot/destination", hostname=HOST, keepalive=600).payload.decode('utf-8')
        return msg
