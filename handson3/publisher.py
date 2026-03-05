import time
import json
import paho.mqtt.client as mqtt

HOST = "139.162.222.115"
PORT = 443
USERNAME = "MATZI"
PASSWORD = "MATZI"

TOPIC = "hit/iot/shaked/test"

def on_connect(client, userdata, flags, rc):
    print("CONNECTED, rc=", rc)

def on_disconnect(client, userdata, rc):
    print("DISCONNECTED, rc=", rc)

client_id = f"shaked_pub_{int(time.time())}"

client = mqtt.Client(client_id=client_id, transport="websockets")
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# אופציונלי: path אם צריך
# client.ws_set_options(path="/mqtt")

print("Connecting...")
client.connect(HOST, PORT, keepalive=60)
client.loop_start()

for i in range(1, 6):
    payload = {
        "sender": "shaked",
        "msg_num": i,
        "text": f"hello from publisher #{i}",
        "ts": time.time()
    }
    data = json.dumps(payload)

    result = client.publish(TOPIC, data, qos=1, retain=False)
    status = result[0]
    print("PUBLISHED" if status == 0 else f"FAILED ({status})", data)

    time.sleep(1)

client.loop_stop()
client.disconnect()
