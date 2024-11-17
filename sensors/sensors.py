from random import randint

import paho.mqtt.client as mqtt
import time
import random
import math

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_FAN_HUMIDITY = 'home/fan/humidity'
MQTT_TOPIC_LIGHT_LUX = 'home/light/lux_value'
MQTT_TOPIC_TEMP_VALUE = 'home/temperature/temperature_value'
MQTT_TOPIC_TEMP_SETTINGS_MAX = 'home/temperature/settings/max_temperature'
MQTT_TOPIC_TEMP_SETTINGS_MIN = 'home/temperature/settings/min_temperature'
MQTT_TOPIC_TEMP_AMPLITUDE = 'home/temperature/settings/amplitude'
MQTT_TOPIC_TEMP_BASE = 'home/temperature/settings/base'
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
temperature_threshold_max = 30
temperature_threshold_min = 10
current_temperature = 20
period = 60
step = 5
time_counter = 0

def on_message(client, userdata, msg):
    global sprayer_threshold, temperature_threshold_max, temperature_threshold_min, amplitude, base_temperature
    if msg.topic == MQTT_TOPIC_SPRAYER_SETTINGS:
        sprayer_threshold = int(msg.payload.decode())
        print(f"New sprayer threshold: {sprayer_threshold}")
    elif msg.topic == MQTT_TOPIC_TEMP_SETTINGS_MAX:
        temperature_threshold_max = int(msg.payload.decode())
        print(f"New sprayer threshold: {temperature_threshold_max}")
    elif msg.topic == MQTT_TOPIC_TEMP_SETTINGS_MIN:
        temperature_threshold_min = int(msg.payload.decode())
        print(f"New sprayer threshold: {temperature_threshold_min}")
    elif msg.topic == MQTT_TOPIC_TEMP_AMPLITUDE:
        amplitude = float(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_TEMP_BASE:
        base_temperature = float(msg.payload.decode())


client.subscribe([(MQTT_TOPIC_SPRAYER_SETTINGS, 0), (MQTT_TOPIC_TEMP_SETTINGS_MAX, 0), (MQTT_TOPIC_TEMP_SETTINGS_MIN, 0), (MQTT_TOPIC_TEMP_AMPLITUDE, 0), (MQTT_TOPIC_TEMP_BASE, 0)])
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
    base_temperature = (temperature_threshold_max + temperature_threshold_min) / 2
    amplitude = (temperature_threshold_max - temperature_threshold_min) / 2 + 0.5
    current_temperature = base_temperature + amplitude * math.sin(2 * math.pi * (time_counter / period))
    current_temperature += (randint(-10, 10))/10

    client.publish(MQTT_TOPIC_TEMP_VALUE, current_temperature)
    client.publish(MQTT_TOPIC_SPRAYER_HUMIDITY, current_sprayer)
    client.publish(MQTT_TOPIC_SPRAYER_INCREASE, decreasing)
    time.sleep(5)
    time_counter += step