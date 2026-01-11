import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT broker details
mqtt_broker = "rule28.i4t.swin.edu.au"
mqtt_port = 1883
mqtt_username = '103796548'
mqtt_password = '103796548'

# MQTT topics to publish to
mqtt_topic_private = f"{mqtt_username}/private"
mqtt_topic_public2 = "public/topic2"

# Create a client instance
client = mqtt.Client()

# Set the username and password
client.username_pw_set(username=mqtt_username, password=mqtt_password)

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, keepalive=60)
client.loop_start()

try:
    while True:
        # Generate random temperature and humidity values
        temperature = round(random.uniform(20, 30), 1)
        humidity = round(random.uniform(40, 60), 1)

        # Create data dictionaries for both topics
        data_private = {"temperature": temperature, "humidity": humidity}
        data_public2 = {"temperature": temperature, "humidity": humidity}

        # Convert data to JSON
        message_private = json.dumps(data_private)
        message_public2 = json.dumps(data_public2)

        # Publish messages to the MQTT topics
        client.publish(mqtt_topic_private, message_private)
        client.publish(mqtt_topic_public2, message_public2)

        print(f"Published message to topic {mqtt_topic_private}: {message_private}")
        print(f"Published message to topic {mqtt_topic_public2}: {message_public2}")

        # Wait for some time before publishing the next message (e.g., 10 seconds)
        time.sleep(10)

except KeyboardInterrupt:
    # Disconnect from the MQTT broker on Ctrl+C
    client.disconnect()
    print("Disconnected from MQTT broker")
