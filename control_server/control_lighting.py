import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_LIGHT = 'home/light'
MQTT_TOPIC_LIGHT_SETTINGS = 'home/light/settings'
MQTT_TOPIC_LIGHT_CONTROL = 'home/light/control'

light_threshold = 300
current_light = 0

def on_connect(client, userdata, flags, rc):
    client.subscribe([(MQTT_TOPIC_LIGHT, 0), (MQTT_TOPIC_LIGHT_SETTINGS, 0)])

def on_message(client, userdata, msg):
    global current_light, light_threshold
    if msg.topic == MQTT_TOPIC_LIGHT:
        current_light = int(msg.payload.decode())
        control_light()
    elif msg.topic == MQTT_TOPIC_LIGHT_SETTINGS:
        light_threshold = int(msg.payload.decode())
        print(f"New light threshold: {light_threshold}")

def control_light():
    if current_light < light_threshold:
        client.publish(MQTT_TOPIC_LIGHT_CONTROL, 'ON')
    else:
        client.publish(MQTT_TOPIC_LIGHT_CONTROL, 'OFF')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()