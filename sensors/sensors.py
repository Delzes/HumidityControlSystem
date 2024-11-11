import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_FAN_HUMIDITY = 'home/fan/humidity'
MQTT_TOPIC_LIGHT_LUX = 'home/light/lux_value'
MQTT_TOPIC_SPRAYER = 'home/sprayer'
MQTT_TOPIC_SPRAYER_HUMIDITY = 'home/sprayer/humidity'
MQTT_TOPIC_SPRAYER_SETTINGS = 'home/sprayer/settings'
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

client.subscribe(MQTT_TOPIC_SPRAYER_SETTINGS, 0)
client.on_message = on_message
client.loop_start()

while True:
    humidity = random.randint(40, 80)
    client.publish(MQTT_TOPIC_FAN_HUMIDITY, humidity)
    light_level = random.randint(100, 1000)  # Симуляция значений от 100 до 1000 Lux
    client.publish(MQTT_TOPIC_LIGHT_LUX, light_level)
    if decreasing:
        current_sprayer -= decrease_step
        if current_sprayer <= sprayer_threshold:
            decreasing = False
    else:
        if current_sprayer > 90:
            current_sprayer += 100 - current_sprayer
        else:
            current_sprayer += increase_step
        if current_sprayer >= 100:
            decreasing = True

    client.publish(MQTT_TOPIC_SPRAYER_HUMIDITY, current_sprayer)
    client.publish(MQTT_TOPIC_SPRAYER_INCREASE, decreasing)
    print(f"Current sprayer: {current_sprayer}%")
    time.sleep(5)