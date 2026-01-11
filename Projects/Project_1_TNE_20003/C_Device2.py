import paho.mqtt.client as mqtt
import json

# MQTT broker details
mqtt_broker = "rule28.i4t.swin.edu.au"
mqtt_port = 1883
mqtt_username = '103796548'
mqtt_password = '103796548'
#client_id = 'mqttx_103796548'


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
client.username_pw_set(username=mqtt_username, password=mqtt_password)

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
