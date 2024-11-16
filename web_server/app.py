from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883

MQTT_TOPIC_FAN_HUMIDITY = 'home/fan/humidity'
MQTT_TOPIC_LIGHT_LUX = 'home/light/lux_value'
MQTT_TOPIC_SPRAYER_HUMIDITY = 'home/sprayer/humidity'
MQTT_TOPIC_TEMP_VALUE = 'home/temperature/temperature_value'
MQTT_TOPIC_FAN_SETTINGS = 'home/fan/settings'
MQTT_TOPIC_LIGHT_SETTINGS = 'home/light/settings'
MQTT_TOPIC_SPRAYER_SETTINGS = 'home/sprayer/settings'
MQTT_TOPIC_TEMP_SETTINGS_MAX = 'home/temperature/settings/max_temperature'
MQTT_TOPIC_TEMP_SETTINGS_MIN = 'home/temperature/settings/min_temperature'

current_humidity = 0
humidity_threshold = 60
current_light = 0
light_threshold = 300
sprayer_threshold = 50
current_sprayer = 100
temperature_threshold_max = 30
temperature_threshold_min = 10
current_temperature = 20

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe([(MQTT_TOPIC_FAN_HUMIDITY, 0), (MQTT_TOPIC_LIGHT_LUX, 0), (MQTT_TOPIC_SPRAYER_HUMIDITY, 0), (MQTT_TOPIC_TEMP_VALUE, 0)])
    client.publish(MQTT_TOPIC_FAN_SETTINGS, str(humidity_threshold))
    client.publish(MQTT_TOPIC_LIGHT_SETTINGS, str(light_threshold))
    client.publish(MQTT_TOPIC_SPRAYER_SETTINGS, str(sprayer_threshold))
    client.publish(MQTT_TOPIC_TEMP_SETTINGS_MIN, str(temperature_threshold_min))
    client.publish(MQTT_TOPIC_TEMP_SETTINGS_MAX, str(temperature_threshold_max))

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload}")
    global current_humidity, current_light, current_sprayer, current_temperature
    if msg.topic == MQTT_TOPIC_FAN_HUMIDITY:
        current_humidity = int(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_LIGHT_LUX:
        current_light = int(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_SPRAYER_HUMIDITY:
        current_sprayer = int(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_TEMP_VALUE:
        current_temperature = round(float(msg.payload.decode()), 2)


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

@app.route('/temperature')
def temperature():
    return render_template('temperature.html', temperature=current_temperature, temperature_threshold_min=temperature_threshold_min, temperature_threshold_max=temperature_threshold_max)

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global humidity_threshold
    humidity_threshold = int(request.form['threshold'])
    mqtt_client.publish(MQTT_TOPIC_FAN_SETTINGS, str(humidity_threshold))
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

@app.route('/update_temperature_threshold_min', methods=['POST'])
def update_temperature_threshold_min():
    global temperature_threshold_min
    temperature_threshold_min = int(request.form['temperature_threshold_min'])
    mqtt_client.publish(MQTT_TOPIC_TEMP_SETTINGS_MIN, str(temperature_threshold_min))
    return jsonify({'status': 'success', 'new_temperature_threshold_min': temperature_threshold_min})

@app.route('/update_temperature_threshold_max', methods=['POST'])
def update_temperature_threshold_max():
    global temperature_threshold_max
    temperature_threshold_max = int(request.form['temperature_threshold_max'])
    mqtt_client.publish(MQTT_TOPIC_TEMP_SETTINGS_MAX, str(temperature_threshold_max))
    return jsonify({'status': 'success', 'new_temperature_threshold_max': temperature_threshold_max})

@app.route('/get_humidity', methods=['GET'])
def get_humidity():
    return jsonify({'humidity': current_humidity})

@app.route('/get_light', methods=['GET'])
def get_light():
    return jsonify({'light': current_light})

@app.route('/get_sprayer', methods=['GET'])
def get_sprayer():
    return jsonify({'sprayer': current_sprayer})

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    return jsonify({'temperature': current_temperature})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)