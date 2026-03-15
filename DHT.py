import sys
import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QLineEdit,
    QPushButton, QFormLayout, QWidget, QCheckBox
)
from PyQt5.QtGui import QIntValidator
import paho.mqtt.client as mqtt
from mqtt_init import *

# Creating Client name - should be unique
global clientname, CONNECTED
CONNECTED = False
r = random.randrange(1, 10000000)
clientname = "IOT_client-Id234-" + str(r)

DHT_topic = "pr/home/shaked_ran/dht/sts"
update_rate = 5000  # in msec


class Mqtt_client:

    def __init__(self):
        self.broker = ''
        self.topic = ''
        self.port = 0
        self.clientname = ''
        self.username = ''
        self.password = ''
        self.subscribeTopic = ''
        self.publishTopic = ''
        self.publishMessage = ''
        self.on_connected_to_form = None
        self.client = None

    # Setters and getters
    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form

    def get_broker(self):
        return self.broker

    def set_broker(self, value):
        self.broker = value

    def get_port(self):
        return self.port

    def set_port(self, value):
        self.port = value

    def get_clientName(self):
        return self.clientname

    def set_clientName(self, value):
        self.clientname = value

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_password(self):
        return self.password

    def set_password(self, value):
        self.password = value

    def get_subscribeTopic(self):
        return self.subscribeTopic

    def set_subscribeTopic(self, value):
        self.subscribeTopic = value

    def get_publishTopic(self):
        return self.publishTopic

    def set_publishTopic(self, value):
        self.publishTopic = value

    def get_publishMessage(self):
        return self.publishMessage

    def set_publishMessage(self, value):
        self.publishMessage = value

    def on_log(self, client, userdata, level, buf):
        print("log: " + buf)

    def on_connect(self, client, userdata, flags, rc):
        global CONNECTED
        if rc == 0:
            print("connected OK")
            CONNECTED = True
            if self.on_connected_to_form:
                self.on_connected_to_form()
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        global CONNECTED
        CONNECTED = False
        print("DisConnected result code " + str(rc))

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("message from:", topic, m_decode)

    def connect_to(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
            client_id=self.clientname,
            clean_session=True
        )
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message

        if self.username or self.password:
            self.client.username_pw_set(self.username, self.password)

        print("Connecting to broker", self.broker)
        self.client.connect(self.broker, self.port)

    def disconnect_from(self):
        if self.client:
            self.client.disconnect()

    def start_listening(self):
        if self.client:
            self.client.loop_start()

    def stop_listening(self):
        if self.client:
            self.client.loop_stop()

    def subscribe_to(self, topic):
        if CONNECTED:
            self.client.subscribe(topic)
        else:
            print("Can't subscribe. Connection should be established first")

    def publish_to(self, topic, message):
        if CONNECTED:
            self.client.publish(topic, message)
        else:
            print("Can't publish. Connection should be established first")


class ConnectionDock(QDockWidget):
    def __init__(self, mc):
        super().__init__()

        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)

        self.eHostInput = QLineEdit()
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(5)
        self.ePort.setText(str(broker_port))

        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(DHT_topic)

        self.Temperature = QLineEdit()
        self.Temperature.setText('')

        self.Humidity = QLineEdit()
        self.Humidity.setText('')

        formLayout = QFormLayout()
        formLayout.addRow("Turn On/Off", self.eConnectbtn)
        formLayout.addRow("Pub topic", self.ePublisherTopic)
        formLayout.addRow("Temperature", self.Temperature)
        formLayout.addRow("Humidity", self.Humidity)

        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()
        mainwin.timer.start(update_rate)

    def push_button_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), '{"value":1}')


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mc = Mqtt_client()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(update_rate)

        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setGeometry(30, 600, 300, 150)
        self.setWindowTitle('DHT')

        self.connectionDock = ConnectionDock(self.mc)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.connectionDock)

    def update_data(self):
        print('Next update')
        temp = 22 + random.randrange(1, 10) / 10
        hum = 74 + random.randrange(1, 25) / 10
        current_data = f'Temperature: {temp} Humidity: {hum}'
        self.connectionDock.Temperature.setText(str(temp))
        self.connectionDock.Humidity.setText(str(hum))
        self.mc.publish_to(DHT_topic, current_data)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
