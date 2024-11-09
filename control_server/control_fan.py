import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_HUMIDITY = 'home/humidity'
MQTT_TOPIC_SETTINGS = 'home/settings'
MQTT_TOPIC_FAN = 'home/fan'

humidity_threshold = 60
current_humidity = 0

def on_connect(client, userdata, flags, rc):
    client.subscribe([(MQTT_TOPIC_HUMIDITY, 0), (MQTT_TOPIC_SETTINGS, 0)])

def on_message(client, userdata, msg):
    global current_humidity, humidity_threshold
    if msg.topic == MQTT_TOPIC_HUMIDITY:
        current_humidity = int(msg.payload.decode())
        control_fan()
    elif msg.topic == MQTT_TOPIC_SETTINGS:
        humidity_threshold = int(msg.payload.decode())

def control_fan():
    if current_humidity > humidity_threshold:
        client.publish(MQTT_TOPIC_FAN, 'ON')
    else:
        client.publish(MQTT_TOPIC_FAN, 'OFF')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()