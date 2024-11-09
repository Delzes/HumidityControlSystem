import paho.mqtt.client as mqtt

from sensors.sprayer_sensor import decreasing

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SPRAYER = 'home/sprayer'
MQTT_TOPIC_SPRAYER_SETTINGS = 'home/sprayer/settings'
MQTT_TOPIC_SPRAYER_CONTROL = 'home/sprayer/control'

sprayer_threshold = 50
current_sprayer = 100

def on_connect(client, userdata, flags, rc):
    client.subscribe([(MQTT_TOPIC_SPRAYER, 0), (MQTT_TOPIC_SPRAYER_SETTINGS, 0)])

def on_message(client, userdata, msg):
    global current_sprayer, sprayer_threshold, decreasing
    if msg.topic == MQTT_TOPIC_SPRAYER:
        current_sprayer = int(msg.payload.decode())
        control_sprayer()
    elif msg.topic == MQTT_TOPIC_SPRAYER_SETTINGS:
        sprayer_threshold = int(msg.payload.decode())
        print(f"New sprayer threshold: {sprayer_threshold}")
    elif msg.topic == MQTT_TOPIC_SPRAYER_SETTINGS:
        decreasing = msg.payload.decode()

def control_sprayer():
    if decreasing:
        client.publish(MQTT_TOPIC_SPRAYER_CONTROL, 'OFF')
    else:
        client.publish(MQTT_TOPIC_SPRAYER_CONTROL, 'ON')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()