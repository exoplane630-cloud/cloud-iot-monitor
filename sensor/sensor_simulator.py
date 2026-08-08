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
resend_needed = False

def initialise_cache():
    with sqlite3.connect(CACHE_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cached_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL
            )
            """
        )

        connection.commit()

def save_to_cache(message):
    with sqlite3.connect(CACHE_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO cached_readings (payload) VALUES (?)",
            (message,)
        )

        connection.commit()

    print("Reading saved to local cache")

def resend_cached_readings(client):
    with sqlite3.connect(CACHE_DB) as connection:
        cursor = connection.cursor()

        cached_rows = cursor.execute(
            "SELECT id, payload FROM cached_readings ORDER BY id"
        ).fetchall()

        if not cached_rows:
            return

        print(f"Found {len(cached_rows)} cached reading(s). Resending...")

        for row_id, payload in cached_rows:
            result = client.publish(TOPIC, payload)

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"Failed to resend cached reading {row_id}")
                break

            result.wait_for_publish()

            if result.is_published():
                cursor.execute(
                    "DELETE FROM cached_readings WHERE id = ?",
                    (row_id,)
                )
                connection.commit()

                print(f"Resent cached reading {row_id}")
            else:
                print(f"Cached reading {row_id} was not confirmed")
                break

def on_connect(client, userdata, flags, reason_code, properties):
    global mqtt_connected
    global resend_needed

    if reason_code == 0:
        mqtt_connected = True
        resend_needed = True
        print("Connected to MQTT broker")
    else:
        mqtt_connected = False
        print(f"Failed to connect to MQTT broker: {reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    global mqtt_connected

    mqtt_connected = False
    print("MQTT connection lost")

initialise_cache()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT)
client.loop_start()

print("Cloud IoT Sensor Simulator started")

while True:
    if mqtt_connected and resend_needed:
        resend_cached_readings(client)
        resend_needed = False

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