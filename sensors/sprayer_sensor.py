import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SPRAYER = 'home/sprayer'
MQTT_TOPIC_SPRAYER_SETTINGS = 'home/sprayer/settings'
MQTT_TOPIC_SPRAYER_CONTROL = 'home/sprayer/control'
MQTT_TOPIC_SPRAYER_INCREASE = 'home/sprayer/increase'

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

current_sprayer = 100
decrease_step = 2
increase_step = 10
sprayer_threshold = 50
decreasing = True

def on_message(client, userdata, msg):
    global sprayer_threshold
    if msg.topic == MQTT_TOPIC_SPRAYER_SETTINGS:
        sprayer_threshold = int(msg.payload.decode())
        print(f"New sprayer threshold: {sprayer_threshold}")


client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC_SPRAYER_SETTINGS)
client.loop_start()

while True:
    client.publish(MQTT_TOPIC_SPRAYER, current_sprayer)
    client.publish(MQTT_TOPIC_SPRAYER_INCREASE, decreasing)

    print(f"Current sprayer: {current_sprayer}%")

    if decreasing:
        current_sprayer -= decrease_step
        if current_sprayer <= sprayer_threshold:
            decreasing = False
    else:
        current_sprayer += increase_step
        if current_sprayer >= 100:
            decreasing = True

    time.sleep(5)