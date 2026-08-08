import sqlite3
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/environment"

CACHE_DB = "cache/sensor_cache.db"

mqtt_connected = False

cache_connection = sqlite3.connect(CACHE_DB)
cache_cursor = cache_connection.cursor()

cache_cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS cached_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payload TEXT NOT NULL
    )
    """
)

cache_connection.commit()

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

def save_to_cache(message):
    cache_cursor.execute(
        "INSERT INTO cached_readings (payload) VALUES (?)",
        (message,)
    )

    cache_connection.commit()

    print("Reading saved to local cache")

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
        print(f"MQTT unavailable: {message}")
        save_to_cache(message)

    time.sleep(5)