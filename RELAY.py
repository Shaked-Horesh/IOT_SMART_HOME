import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QLineEdit,
    QPushButton, QFormLayout, QWidget, QCheckBox
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
import paho.mqtt.client as mqtt
from mqtt_init import *

global clientname, ON
clientname = "IOT_client-Relay-123"
relay_topic = "pr/home/shaked_ran/relay/cmnd"
ON = False


class Mqtt_client:

    def __init__(self):
        self.broker = ''
        self.port = 0
        self.clientname = ''
        self.username = ''
        self.password = ''
        self.subscribeTopic = ''
        self.on_connected_to_form = None
        self.client = None

    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form

    def set_broker(self, value):
        self.broker = value

    def set_port(self, value):
        self.port = value

    def set_clientName(self, value):
        self.clientname = value

    def set_username(self, value):
        self.username = value

    def set_password(self, value):
        self.password = value

    def on_log(self, client, userdata, level, buf):
        print("log:", buf)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
            if self.on_connected_to_form:
                self.on_connected_to_form()
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code", rc)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = msg.payload.decode("utf-8", "ignore")
        print("message from:", topic, m_decode)
        mainwin.connectionDock.update_btn_state(m_decode)

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

    def start_listening(self):
        if self.client:
            self.client.loop_start()

    def subscribe_to(self, topic):
        if self.client:
            self.client.subscribe(topic)


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
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eSSL = QCheckBox()
        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(relay_topic)

        self.ePushtbtn = QPushButton("", self)
        self.ePushtbtn.setStyleSheet("background-color: gray")

        formLayout = QFormLayout()
        formLayout.addRow("Turn On/Off", self.eConnectbtn)
        formLayout.addRow("Sub topic", self.eSubscribeTopic)
        formLayout.addRow("Status", self.ePushtbtn)

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
        self.mc.subscribe_to(self.eSubscribeTopic.text())

    def update_btn_state(self, text):
        global ON
        if ON:
            self.ePushtbtn.setStyleSheet("background-color: gray")
            ON = False
        else:
            self.ePushtbtn.setStyleSheet("background-color: red")
            ON = True


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mc = Mqtt_client()
        self.setGeometry(30, 300, 300, 150)
        self.setWindowTitle("RELAY")

        self.connectionDock = ConnectionDock(self.mc)
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
