import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "shaked_ran/smartvacuum/sensors/distance"

distance_values = [100, 80, 60, 40, 25, 15, 10, 5]


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="obstacle_sensor_emulator")
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("Obstacle sensor started...")

    while True:
        for value in distance_values:
            client.publish(TOPIC, str(value))
            print(f"Published obstacle distance: {value} cm")
            time.sleep(3)


if __name__ == "__main__":
    main()