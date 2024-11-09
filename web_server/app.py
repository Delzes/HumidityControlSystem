from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_HUMIDITY = 'home/humidity'
MQTT_TOPIC_SETTINGS = 'home/settings'

current_humidity = 0
humidity_threshold = 60

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC_HUMIDITY)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload}")
    global current_humidity
    current_humidity = int(msg.payload.decode())

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('index.html', humidity=current_humidity, threshold=humidity_threshold)

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global humidity_threshold
    humidity_threshold = int(request.form['threshold'])
    mqtt_client.publish(MQTT_TOPIC_SETTINGS, str(humidity_threshold))
    return jsonify({'status': 'success', 'new_threshold': humidity_threshold})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)