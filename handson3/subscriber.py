import time
import paho.mqtt.client as mqtt

HOST = "test.mosquitto.org"  #ציבורי
PORT = 1883
USERNAME = None
PASSWORD = None

TOPIC = "hit/iot/shakedhoresh/handson3/demo1"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("CONNECTED, rc=", reason_code)
    if reason_code == 0:
        client.subscribe(TOPIC, qos=1)
        print("SUBSCRIBED to:", TOPIC)

def on_message(client, userdata, msg):
    print(f"RECEIVED topic={msg.topic} qos={msg.qos} payload={msg.payload.decode(errors='ignore')}")

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    print("DISCONNECTED, rc=", reason_code)

client_id = f"shaked_sub_{int(time.time())}"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

if USERNAME and PASSWORD:
    client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print(f"Connecting to {HOST}:{PORT} ...")
client.connect(HOST, PORT, keepalive=60)
client.loop_forever()
