import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT broker details
mqtt_broker = "rule28.i4t.swin.edu.au"
mqtt_port = 1883
mqtt_username = '103796548'
mqtt_password = '103796548'

# MQTT topics
mqtt_publish_topic = f"{mqtt_username}/private"
mqtt_publish_topic2 = "public/topic2"
mqtt_subscribe_topics = [f"{mqtt_username}/private", "public/topic2"]

# Callback when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    print(f"Received message from topic {message.topic}: {data}")

# Create a client instance
client = mqtt.Client()

# Set the callback function for when a message is received
client.on_message = on_message

client.username_pw_set(username=mqtt_username, password=mqtt_password)

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, keepalive=60)

# Subscribe to the specified MQTT topics
for topic in mqtt_subscribe_topics:
    client.subscribe(topic)

# Start the MQTT client loop to listen for messages
client.loop_start()

try:
    while True:
        # Generate random temperature and humidity values
        temperature = round(random.uniform(20, 30), 1)
        humidity = round(random.uniform(40, 60), 1)

        # Create data dictionaries for both topics
        data = {"temperature": temperature, "humidity": humidity}

        # Convert data to JSON
        message = json.dumps(data)

        # Publish the message to the MQTT topics
        client.publish(mqtt_publish_topic, message)
        client.publish(mqtt_publish_topic2, message)

        print(f"Published message to topic {mqtt_publish_topic}: {message}")
        print(f"Published message to topic {mqtt_publish_topic2}: {message}")

        # Wait for some time before publishing the next message (e.g., 10 seconds)
        time.sleep(10)

except KeyboardInterrupt:
    # Disconnect from the MQTT broker on Ctrl+C
    client.disconnect()
    print("Disconnected from MQTT broker")
