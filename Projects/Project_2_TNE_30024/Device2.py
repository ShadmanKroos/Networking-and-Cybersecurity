import paho.mqtt.client as mqtt
import json
import argparse
import sys

# MQTT broker details
mqtt_broker = "136.186.230.88"
mqtt_port = 8883
mqtt_username = '103796548'
mqtt_password = '103796548'

# Parse command-line arguments for CA certificate, client certificate, and key
parser = argparse.ArgumentParser(description="MQTT subscriber with TLS configuration")
parser.add_argument("-ca_cert", required=True, help="Path to the CA certificate file")
parser.add_argument("-client_cert", required=True, help="Path to the client certificate file")
parser.add_argument("-client_key", required=True, help="Path to the client key file")
args = parser.parse_args()

# Verify all required arguments are provided
if not args.ca_cert or not args.client_cert or not args.client_key:
    print("Error: Missing required certificate or key file arguments.")
    sys.exit(1)

# MQTT topics to subscribe to
mqtt_topics = [f"{mqtt_username}/private", "public/topic2"]

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

# Configure TLS for secure communication
client.tls_set(
    ca_certs=args.ca_cert,          # Path to CA certificate
    certfile=args.client_cert,       # Path to client certificate
    keyfile=args.client_key          # Path to client key
)
client.tls_insecure_set(False)  # Enforce certificate validation

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, keepalive=60)

# Subscribe to the specified MQTT topics
for topic in mqtt_topics:
    client.subscribe(topic)

# Start the MQTT client loop to listen for messages
client.loop_start()

try:
    while True:
        pass  # Continue running and listening for messages

except KeyboardInterrupt:
    # Disconnect from the MQTT broker on Ctrl+C
    client.disconnect()
    print("Disconnected from MQTT broker")
