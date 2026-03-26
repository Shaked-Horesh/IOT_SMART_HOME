import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "shaked_ran/smartvacuum/sensors/cliff"

cliff_values = [0, 0, 0, 0, 1, 0, 0]


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="cliff_sensor_emulator")
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("Cliff sensor started...")

    while True:
        for value in cliff_values:
            client.publish(TOPIC, str(value))
            print(f"Published cliff status: {value}")
            time.sleep(4)


if __name__ == "__main__":
    main()