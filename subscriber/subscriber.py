import json

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/environment"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT broker")
    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    sensor_data = json.loads(payload)

    print("----------------------------")
    print(f"Device:      {sensor_data['device_id']}")
    print(f"Temperature: {sensor_data['temperature']} °C")
    print(f"Humidity:    {sensor_data['humidity']} %")
    print(f"Timestamp:   {sensor_data['timestamp']}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("MQTT Subscriber started")

client.loop_forever()