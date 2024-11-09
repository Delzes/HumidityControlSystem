import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    if msg.payload.decode() == 'ON':
        print("Sprayer is ON")
    elif msg.payload.decode() == 'OFF':
        print("Sprayer is OFF")

client = mqtt.Client()
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.subscribe('home/sprayer')
client.loop_forever()
