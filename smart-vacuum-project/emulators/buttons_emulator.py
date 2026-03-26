import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "shaked_ran/smartvacuum/control/button"


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="buttons_emulator")
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("Buttons emulator started...")
    print("Available commands: start, pause, dock, reset_alarm")
    print("Type 'exit' to stop")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            break

        if command in ["start", "pause", "dock", "reset_alarm"]:
            client.publish(TOPIC, command)
            print(f"Published button command: {command}")
        else:
            print("Invalid command")

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()