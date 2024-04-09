import paho.mqtt.publish as publish

HOST = "192.168.0.69"

publish.single("bot/destination", "Esplanade", hostname=HOST)