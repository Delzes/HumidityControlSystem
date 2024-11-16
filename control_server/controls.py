import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_FAN = 'home/fan'
MQTT_TOPIC_LIGHT = 'home/light'
MQTT_TOPIC_SPRAYER = 'home/sprayer'
MQTT_TOPIC_TEMP = 'home/temperature'
MQTT_TOPIC_FAN_HUMIDITY = 'home/fan/humidity'
MQTT_TOPIC_LIGHT_LUX = 'home/light/lux_value'
MQTT_TOPIC_SPRAYER_HUMIDITY = 'home/sprayer/humidity'
MQTT_TOPIC_TEMP_VALUE = 'home/temperature/temperature_value'
MQTT_TOPIC_FAN_SETTINGS = 'home/fan/settings'
MQTT_TOPIC_LIGHT_SETTINGS = 'home/light/settings'
MQTT_TOPIC_SPRAYER_SETTINGS = 'home/sprayer/settings'
MQTT_TOPIC_TEMP_SETTINGS = 'home/temperature/settings'
MQTT_TOPIC_SPRAYER_INCREASE = 'home/sprayer/increase'

humidity_threshold = 60
current_humidity = 0
light_threshold = 300
current_light = 0
sprayer_threshold = 50
current_sprayer = 100
temperature_threshold_max = 30
temperature_threshold_min = 10
current_temperature = 20
decreasing = True

def on_connect(client, userdata, flags, rc):
    client.subscribe([(MQTT_TOPIC_FAN_HUMIDITY, 0), (MQTT_TOPIC_FAN_SETTINGS, 0),(MQTT_TOPIC_LIGHT_LUX, 0), (MQTT_TOPIC_LIGHT_SETTINGS, 0), (MQTT_TOPIC_SPRAYER_HUMIDITY, 0), (MQTT_TOPIC_SPRAYER_SETTINGS, 0), (MQTT_TOPIC_SPRAYER_INCREASE, 0), (MQTT_TOPIC_TEMP_VALUE, 0), (MQTT_TOPIC_TEMP_SETTINGS, 0)])

def on_message(client, userdata, msg):
    global current_humidity, humidity_threshold, current_light, light_threshold, current_sprayer, sprayer_threshold, current_temperature,decreasing
    if msg.topic == MQTT_TOPIC_FAN_HUMIDITY:
        current_humidity = int(msg.payload.decode())
        control_fan()
    elif msg.topic == MQTT_TOPIC_FAN_SETTINGS:
        humidity_threshold = int(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_LIGHT_LUX:
        current_light = int(msg.payload.decode())
        control_light()
    elif msg.topic == MQTT_TOPIC_LIGHT_SETTINGS:
        light_threshold = int(msg.payload.decode())
        print(f"New light threshold: {light_threshold}")
    elif msg.topic == MQTT_TOPIC_SPRAYER_HUMIDITY:
        current_sprayer = int(msg.payload.decode())
        control_sprayer()
    elif msg.topic == MQTT_TOPIC_SPRAYER_SETTINGS:
        sprayer_threshold = int(msg.payload.decode())
        print(f"New sprayer threshold: {sprayer_threshold}")
    elif msg.topic == MQTT_TOPIC_SPRAYER_INCREASE:
        decreasing = msg.payload.decode()


def control_fan():
    if current_humidity > humidity_threshold:
        client.publish(MQTT_TOPIC_FAN, 'ON')
    else:
        client.publish(MQTT_TOPIC_FAN, 'OFF')

def control_light():
    if current_light < light_threshold:
        client.publish(MQTT_TOPIC_LIGHT, 'ON')
    else:
        client.publish(MQTT_TOPIC_LIGHT, 'OFF')

def control_sprayer():
    if decreasing:
        client.publish(MQTT_TOPIC_SPRAYER, 'OFF')
    else:
        client.publish(MQTT_TOPIC_SPRAYER, 'ON')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()