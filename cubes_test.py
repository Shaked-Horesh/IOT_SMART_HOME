import paho.mqtt.client as mqtt
import time
import random

broker = "broker.hivemq.com"
port = 1883
running_time = 120

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
        client.subscribe("pr/home/shaked_ran/#")
        print("subscribed to pr/home/shaked_ran/#")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("DisConnected result code " + str(rc))

def on_message(client, userdata, msg):
    m_decode = msg.payload.decode("utf-8", "ignore")
    print("topic:", msg.topic)
    print("message received:", m_decode)
    print("-------------------")

r = random.randrange(1, 10000)
clientname = "IOT_test-" + str(r)

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1,
    client_id=clientname,
    clean_session=True
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Connecting to broker", broker)
client.connect(broker, port)

client.loop_start()
time.sleep(running_time)
client.loop_stop()
client.disconnect()
print("End of script run")
