import paho.mqtt.client as mqtt

MQTT_TOPIC_FAN = 'home/fan'
MQTT_TOPIC_LIGHT = 'home/light'
MQTT_TOPIC_SPRAYER = 'home/sprayer'

def on_connect(client, userdata, flags, rc):
    client.subscribe([(MQTT_TOPIC_LIGHT, 0), (MQTT_TOPIC_SPRAYER, 0), (MQTT_TOPIC_FAN, 0)])


def on_message(client, userdata, msg):
    if msg.topic == MQTT_TOPIC_FAN:
        if msg.payload.decode() == 'ON':
            print("Fan is ON")
        elif msg.payload.decode() == 'OFF':
            print("Fan is OFF")
    elif msg.topic == MQTT_TOPIC_LIGHT:
        if msg.payload.decode() == 'ON':
            print("Light is ON")
        elif msg.payload.decode() == 'OFF':
            print("Light is OFF")
    elif msg.topic == MQTT_TOPIC_SPRAYER:
        if msg.payload.decode() == 'ON':
            print("Sprayer is ON")
        elif msg.payload.decode() == 'OFF':
            print("Sprayer is OFF")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever()