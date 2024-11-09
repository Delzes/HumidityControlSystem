import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_HUMIDITY = 'home/humidity'

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    humidity = random.randint(40, 80)
    client.publish(MQTT_TOPIC_HUMIDITY, humidity)
    time.sleep(5)
