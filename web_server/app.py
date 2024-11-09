from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_HUMIDITY = 'home/humidity'
MQTT_TOPIC_SETTINGS = 'home/settings'
MQTT_TOPIC_LIGHT = 'home/light'
MQTT_TOPIC_LIGHT_SETTINGS = 'home/light/settings'
MQTT_TOPIC_SPRAYER = 'home/sprayer'
MQTT_TOPIC_SPRAYER_SETTINGS = 'home/sprayer/settings'

current_humidity = 0
humidity_threshold = 60
current_light = 0
light_threshold = 300
sprayer_threshold = 50
current_sprayer = 100

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe([(MQTT_TOPIC_HUMIDITY, 0), (MQTT_TOPIC_LIGHT, 0), (MQTT_TOPIC_SPRAYER, 0)])

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload}")
    global current_humidity, current_light, current_sprayer
    if msg.topic == MQTT_TOPIC_HUMIDITY:
        current_humidity = int(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_LIGHT:
        current_light = int(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_SPRAYER:
        current_sprayer = int(msg.payload.decode())

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('index.html', humidity=current_humidity, threshold=humidity_threshold)

@app.route('/light')
def light():
    return render_template('light.html', light_level=current_light, light_threshold=light_threshold)

@app.route('/sprayer')
def sprayer():
    return render_template('sprayer.html', sprayer=current_sprayer, sprayer_threshold=sprayer_threshold)

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global humidity_threshold
    humidity_threshold = int(request.form['threshold'])
    mqtt_client.publish(MQTT_TOPIC_SETTINGS, str(humidity_threshold))
    return jsonify({'status': 'success', 'new_threshold': humidity_threshold})

@app.route('/update_light_threshold', methods=['POST'])
def update_light_threshold():
    global light_threshold
    light_threshold = int(request.form['light_threshold'])
    mqtt_client.publish(MQTT_TOPIC_LIGHT_SETTINGS, str(light_threshold))
    return jsonify({'status': 'success', 'new_light_threshold': light_threshold})

@app.route('/update_sprayer_threshold', methods=['POST'])
def update_sprayer_threshold():
    global sprayer_threshold
    sprayer_threshold = int(request.form['sprayer_threshold'])
    mqtt_client.publish(MQTT_TOPIC_SPRAYER_SETTINGS, str(sprayer_threshold))
    return jsonify({'status': 'success', 'new_sprayer_threshold': sprayer_threshold})

@app.route('/get_humidity', methods=['GET'])
def get_humidity():
    return jsonify({'humidity': current_humidity})

@app.route('/get_light', methods=['GET'])
def get_light():
    return jsonify({'light': current_light})

@app.route('/get_sprayer', methods=['GET'])
def get_sprayer():
    return jsonify({'sprayer': current_sprayer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)