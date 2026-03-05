import time
import json
import paho.mqtt.client as mqtt

HOST = "test.mosquitto.org"  #ציבורי
PORT = 1883
USERNAME = None
PASSWORD = None

TOPIC = "hit/iot/shakedhoresh/handson3/demo1"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("CONNECTED, rc=", reason_code)

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    print("DISCONNECTED, rc=", reason_code)

client_id = f"shaked_pub_{int(time.time())}"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

if USERNAME and PASSWORD:
    client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

print(f"Connecting to {HOST}:{PORT} ...")
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
    info = client.publish(TOPIC, data, qos=1, retain=False)
    print("PUBLISH rc=", info.rc, "mid=", info.mid, "payload=", data)
    time.sleep(1)

client.loop_stop()
client.disconnect()
