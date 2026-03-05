import time
import paho.mqtt.client as mqtt

HOST = "139.162.222.115"
PORT = 443
USERNAME = "MATZI"
PASSWORD = "MATZI"

TOPIC = "hit/iot/shaked/test"   # אפשר לשנות, אבל להשאיר עקבי בין שניהם

def on_connect(client, userdata, flags, rc):
    # rc == 0 זה הצלחה
    print("CONNECTED, rc=", rc)
    if rc == 0:
        client.subscribe(TOPIC, qos=1)
        print("SUBSCRIBED to:", TOPIC)

def on_message(client, userdata, msg):
    print(f"RECEIVED topic={msg.topic} qos={msg.qos} payload={msg.payload.decode(errors='ignore')}")

def on_disconnect(client, userdata, rc):
    print("DISCONNECTED, rc=", rc)

client_id = f"shaked_sub_{int(time.time())}"

client = mqtt.Client(client_id=client_id, transport="websockets")  # חשוב ל-443
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# אם אצלכם צריך path אחר ל-websocket, לפעמים זה "/mqtt"
# client.ws_set_options(path="/mqtt")

print("Connecting...")
client.connect(HOST, PORT, keepalive=60)

client.loop_forever()
