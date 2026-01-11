import paho.mqtt.client as mqtt
import time
import json
import random
import argparse
import sys

# MQTT broker details
mqtt_broker = "136.186.230.88"
mqtt_port = 8883  # Secure MQTT port
mqtt_username = '103796548'
mqtt_password = '103796548'

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MQTT client configuration")
parser.add_argument("-ca_cert", required=True, help="Path to the CA certificate file")
parser.add_argument("-client_cert", required=True, help="Path to the client certificate file")
parser.add_argument("-client_key", required=True, help="Path to the client key file")
args = parser.parse_args()

# Check that all required arguments are provided
if not args.ca_cert or not args.client_cert or not args.client_key:
    print("Error: Missing required certificate or key file arguments.")
    sys.exit(1)

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

# Set the username and password for MQTT broker authentication
client.username_pw_set(username=mqtt_username, password=mqtt_password)

# Configure TLS for secure communication with CA, client cert, and key
client.tls_set(
    ca_certs=args.ca_cert,          # Path to CA certificate
    certfile=args.client_cert,       # Path to client certificate
    keyfile=args.client_key          # Path to client key
)

# Optional: Set TLS version and validation flags
client.tls_insecure_set(False)  # Ensures the certificate is validated

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
