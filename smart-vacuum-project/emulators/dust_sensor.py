import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "shaked_ran/smartvacuum/sensors/dust"

dust_values = [10, 20, 35, 50, 65, 80, 90, 95]


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="dust_sensor_emulator")
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("Dust sensor started...")

    while True:
        for value in dust_values:
            client.publish(TOPIC, str(value))
            print(f"Published dust level: {value}%")
            time.sleep(3)


if __name__ == "__main__":
    main()