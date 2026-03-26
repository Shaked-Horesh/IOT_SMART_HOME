import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "shaked_ran/smartvacuum/sensors/battery"

battery_values = [100, 90, 80, 70, 60, 50, 40, 30, 20, 15, 10]


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="battery_sensor_emulator")
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("Battery sensor started...")

    while True:
        for value in battery_values:
            client.publish(TOPIC, str(value))
            print(f"Published battery level: {value}%")
            time.sleep(3)


if __name__ == "__main__":
    main()