import json

import os
from dotenv import load_dotenv

import paho.mqtt.client as mqtt
import psycopg2

load_dotenv()

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/environment"

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "iotdb"
DB_USER = "iotuser"
DB_PASSWORD = "iotpassword"

db_connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

db_cursor = db_connection.cursor()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker")

        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")

    else:
        print(f"MQTT connection failed: {reason_code}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    sensor_data = json.loads(payload)

    print("----------------------------")
    print(f"Device:      {sensor_data['device_id']}")
    print(f"Temperature: {sensor_data['temperature']} °C")
    print(f"Humidity:    {sensor_data['humidity']} %")
    print(f"Timestamp:   {sensor_data['timestamp']}")

    db_cursor.execute(
        """
        INSERT INTO sensor_readings (
            device_id,
            temperature,
            humidity,
            timestamp
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            sensor_data["device_id"],
            sensor_data["temperature"],
            sensor_data["humidity"],
            sensor_data["timestamp"]
        )
    )

    db_connection.commit()

    print("Saved to PostgreSQL")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("MQTT Subscriber started")

client.loop_forever()