import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/environment"

mqtt_connected = False


def on_connect(client, userdata, flags, reason_code, properties):
    global mqtt_connected

    if reason_code == 0:
        mqtt_connected = True
        print("Connected to MQTT broker")
    else:
        mqtt_connected = False
        print(f"Failed to connect to MQTT broker: {reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    global mqtt_connected

    mqtt_connected = False
    print("MQTT connection lost")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT)
client.loop_start()

print("Cloud IoT Sensor Simulator started")

while True:
    temperature = round(random.uniform(20.0, 30.0), 1)
    humidity = round(random.uniform(40.0, 70.0), 1)
    timestamp = datetime.now().isoformat(timespec="seconds")

    sensor_data = {
        "device_id": "sensor-01",
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp
    }

    message = json.dumps(sensor_data)

    if mqtt_connected:
        result = client.publish(TOPIC, message)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Published to {TOPIC}: {message}")
        else:
            print("Failed to publish MQTT message")
    else:
        print(f"MQTT unavailable - reading not sent: {message}")

    time.sleep(5)