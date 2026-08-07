import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/environment"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

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

    client.publish(TOPIC, message)

    print(f"Published to {TOPIC}: {message}")

    time.sleep(5)