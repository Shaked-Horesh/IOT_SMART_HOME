import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

MOTOR_TOPIC = "shaked_ran/smartvacuum/actuator/motor"
ALARM_TOPIC = "shaked_ran/smartvacuum/actuator/alarm"
DOCK_TOPIC = "shaked_ran/smartvacuum/actuator/dock"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Actuator emulator connected")
    client.subscribe(MOTOR_TOPIC)
    client.subscribe(ALARM_TOPIC)
    client.subscribe(DOCK_TOPIC)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received actuator command on {msg.topic}: {payload}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="actuator_emulator")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()