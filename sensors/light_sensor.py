import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_LIGHT = 'home/light'

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    light_level = random.randint(100, 1000)  # Симуляция значений от 100 до 1000 Lux
    client.publish(MQTT_TOPIC_LIGHT, light_level)
    time.sleep(5)
