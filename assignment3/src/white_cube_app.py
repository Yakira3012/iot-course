import os
import sys
import PyQt5
import random
import json
import winsound
import datetime
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import time

# Creating Client name - should be unique
global clientname
r = random.randrange(1, 10000)
clientname = "IOT_clientId-nXLMZeDcjH" + str(r)


# --- Thread-safe bridge: paho fires on_message on its own thread;
#     this QObject carries the payload to the main thread via Qt signals ---
class MqttSignals(QObject):
    message_received = pyqtSignal(str, str)   # topic, payload
    connected = pyqtSignal()
    disconnected = pyqtSignal()


class Mqtt_client():

    def __init__(self):
        self.broker = ''
        self.topic = 'matzi/all'
        self.port = '1883'
        self.clientname = ''
        self.username = ''
        self.password = ''
        self.subscribeTopic = ''
        self.publishTopic = ''
        self.publishMessage = ''
        self.on_connected_to_form = None
        self.on_disconnected_to_form = None
        self.signals = MqttSignals()

    # --- Setters and getters (kept from professor's template) ---
    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form
    def set_on_disconnected_to_form(self, cb):
        self.on_disconnected_to_form = cb
    def get_broker(self):       return self.broker
    def set_broker(self, value):    self.broker = value
    def get_port(self):         return self.port
    def set_port(self, value):      self.port = value
    def get_clientName(self):   return self.clientname
    def set_clientName(self, value): self.clientname = value
    def get_username(self):     return self.username
    def set_username(self, value):  self.username = value
    def get_password(self):     return self.password
    def set_password(self, value):  self.password = value
    def get_subscribeTopic(self):   return self.subscribeTopic
    def set_subscribeTopic(self, value): self.subscribeTopic = value
    def get_publishTopic(self):     return self.publishTopic
    def set_publishTopic(self, value):   self.publishTopic = value
    def get_publishMessage(self):   return self.publishMessage
    def set_publishMessage(self, value): self.publishMessage = value

    def on_log(self, client, userdata, level, buf):
        print("log: " + buf)

    # Updated to paho 2.x VERSION2 signature
    def on_connect(self, client, userdata, connect_flags, reason_code, properties):
        if not reason_code.is_failure:
            print("connected OK")
            self.signals.connected.emit()
        else:
            print("Bad connection:", reason_code)

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        print("DisConnected:", reason_code)
        self.signals.disconnected.emit()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("message from:" + topic, m_decode)
        # Route to GUI via signal (thread-safe) — UnTNL fixed
        self.signals.message_received.emit(topic, m_decode)

    def connect_to(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            self.clientname,
            clean_session=True,
            protocol=mqtt.MQTTv311,
        )
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        if self.username:
            self.client.username_pw_set(self.username, self.password)
        print("Connecting to broker ", self.broker)
        self.client.connect(self.broker, self.port)   # UnTNL fixed

    def disconnect_from(self):
        self.client.disconnect()
        print("disconnected")

    def start_listening(self):
        self.client.loop_start()

    def stop_listening(self):
        self.client.loop_stop()

    def subscribe_to(self, topic):
        self.client.subscribe(topic)

    def publish_to(self, topic, message):
        self.client.publish(topic, message)

    def relay_on(self, topic="matzi/0/", device_ID="3PI_16168238", on=True):
        if on:
            self.client.publish(topic + device_ID,
                ' {"type":"set_state", "action":"set_value", "addr":0, "cname":"ONOFF", "value":1}')
        else:
            self.client.publish(topic + device_ID,
                ' {"type":"set_state", "action":"set_value", "addr":0, "cname":"ONOFF", "value":0}')


class MainDock(QDockWidget):
    """Connection dock — based on professor's MainDock, extended with
       running time and connection status indicator."""

    def __init__(self, mc):
        QDockWidget.__init__(self)

        self.mc = mc

        # Host: plain text field so hostnames work (not just IPs)
        self.eHostInput = QLineEdit()
        self.eHostInput.setText("localhost")

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(5)
        self.ePort.setText("1883")

        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText("")

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText("")

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        # Running time: 0 = endless
        self.eRunTime = QLineEdit()
        self.eRunTime.setValidator(QIntValidator())
        self.eRunTime.setText("0")
        self.eRunTime.setToolTip("Seconds before auto-disconnect (0 = endless)")

        self.eSSL = QCheckBox()
        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.is_connected = False
        self.eConnectbtn = QPushButton("Connect", self)
        self.eConnectbtn.setToolTip("click me to connect / disconnect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: red")

        # Connection status indicator
        self.eStatusLabel = QLabel("Disconnected")
        self.eStatusLabel.setStyleSheet("color: red; font-weight: bold")

        self.eEtaLabel = QLabel("")
        self.eEtaLabel.setStyleSheet("color: gray; font-weight: bold")

        statusRow = QWidget()
        statusRowLayout = QHBoxLayout(statusRow)
        statusRowLayout.setContentsMargins(0, 0, 0, 0)
        statusRowLayout.addWidget(self.eStatusLabel)
        statusRowLayout.addWidget(self.eEtaLabel)
        statusRowLayout.addStretch()

        # Single-shot: fires when run time expires → disconnect
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_time_expired)

        # 1-second tick: updates the ETA countdown label
        self.countdown_timer = QTimer()
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.on_countdown_tick)
        self.remaining_seconds = 0

        formLayot = QFormLayout()
        formLayot.addRow("Host", self.eHostInput)
        formLayot.addRow("Port", self.ePort)
        formLayot.addRow("Client ID", self.eClientID)
        formLayot.addRow("User Name", self.eUserName)
        formLayot.addRow("Password", self.ePassword)
        formLayot.addRow("Keep Alive", self.eKeepAlive)
        formLayot.addRow("Run Time (s)", self.eRunTime)
        formLayot.addRow("SSL", self.eSSL)
        formLayot.addRow("Clean Session", self.eCleanSession)
        formLayot.addRow("", self.eConnectbtn)
        formLayot.addRow("Status", statusRow)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)

    def on_connected(self):
        self.is_connected = True
        self.eConnectbtn.setText("Disconnect")
        self.eConnectbtn.setStyleSheet("background-color: green")
        self.eStatusLabel.setText("Connected")
        self.eStatusLabel.setStyleSheet("color: green; font-weight: bold")
        run_time = int(self.eRunTime.text()) if self.eRunTime.text() else 0
        if run_time > 0:
            self.remaining_seconds = run_time
            self.eEtaLabel.setText(f"— {self.remaining_seconds}s")
            self.eEtaLabel.setStyleSheet("color: orange; font-weight: bold")
            self.timer.start(run_time * 1000)
            self.countdown_timer.start()
        else:
            self.eEtaLabel.setText("")

    def on_countdown_tick(self):
        self.remaining_seconds -= 1
        if self.remaining_seconds > 0:
            self.eEtaLabel.setText(f"— {self.remaining_seconds}s")
        else:
            self.eEtaLabel.setText("— 0s")
            self.countdown_timer.stop()

    def on_disconnected(self):
        self.is_connected = False
        self.eConnectbtn.setText("Connect")
        self.eConnectbtn.setStyleSheet("background-color: red")
        self.eStatusLabel.setText("Disconnected")
        self.eStatusLabel.setStyleSheet("color: red; font-weight: bold")
        self.timer.stop()
        self.countdown_timer.stop()
        self.eEtaLabel.setText("")
        self.eEtaLabel.setStyleSheet("color: gray; font-weight: bold")

    def on_time_expired(self):
        self.mc.stop_listening()
        self.mc.disconnect_from()

    def on_button_connect_click(self):
        if self.is_connected:
            self.mc.stop_listening()
            self.mc.disconnect_from()
        else:
            self.mc.set_broker(self.eHostInput.text())
            self.mc.set_port(int(self.ePort.text()))
            self.mc.set_clientName(self.eClientID.text())
            self.mc.set_username(self.eUserName.text())
            self.mc.set_password(self.ePassword.text())
            print('on_button_connect_click')
            self.mc.connect_to()
            self.mc.start_listening()


class PublishDock(QDockWidget):
    """Publisher — unchanged from professor's template."""

    def __init__(self, mc):
        QDockWidget.__init__(self)

        self.mc = mc
        formLayot = QFormLayout()

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText("test/reed")

        self.eQOS = QComboBox()
        self.eQOS.addItems(["0", "1", "2"])
        self.ePublishButton = QPushButton("Publish", self)
        self.eRetainCheckbox = QCheckBox()
        self.eMessageBox = QPlainTextEdit()

        formLayot.addRow("Topic", self.ePublisherTopic)
        formLayot.addRow("QOS", self.eQOS)
        formLayot.addRow("Retain", self.eRetainCheckbox)
        formLayot.addRow("Message", self.eMessageBox)
        formLayot.addRow("", self.ePublishButton)

        self.ePublishButton.clicked.connect(self.on_button_publish_click)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Publish")

    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")
        QTimer.singleShot(500, lambda: self.ePublishButton.setStyleSheet(""))


class SubscribeDock(QDockWidget):
    """Subscribe — UnTNL fixed: update_mess_win now appends to received window."""

    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc

        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText("#")
        self.is_subscribed = False
        self.eSubscribeButton = QPushButton("Subscribe", self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)

        self.eQOS = QComboBox()
        self.eQOS.addItems(["0", "1", "2"])

        self.eRecMess = QTextEdit()
        self.eRecMess.setReadOnly(True)

        formLayot = QFormLayout()
        formLayot.addRow("Topic", self.eSubscribeTopic)
        formLayot.addRow("QOS", self.eQOS)
        formLayot.addRow("Received", self.eRecMess)
        formLayot.addRow("", self.eSubscribeButton)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Subscribe")

    def on_button_subscribe_click(self):
        if self.is_subscribed:
            self.mc.client.unsubscribe(self.eSubscribeTopic.text())
            self.is_subscribed = False
            self.eSubscribeButton.setText("Subscribe")
            self.eSubscribeButton.setStyleSheet("")
        else:
            print(self.eSubscribeTopic.text())
            self.mc.subscribe_to(self.eSubscribeTopic.text())
            self.is_subscribed = True
            self.eSubscribeButton.setText("Unsubscribe")
            self.eSubscribeButton.setStyleSheet("background-color: yellow")

    def update_mess_win(self, text):
        self.eRecMess.append(text)   # UnTNL fixed


class EventHandlerDock(QDockWidget):
    """Reed sensor event handler — new for this assignment."""

    def __init__(self):
        QDockWidget.__init__(self)

        self.eDeviceID = QLineEdit()
        self.eDeviceID.setPlaceholderText("e.g. 3PI_16168238  (blank = all devices)")
        self.eEnableCheck = QCheckBox("Enable event handler")
        self.eSoundCheck = QCheckBox("Sound alarm on state change")
        self.eSoundCheck.setChecked(True)

        self.eStateLabel = QLabel("Door: UNKNOWN")
        self.eStateLabel.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: gray; padding: 4px;"
        )

        self.eAlertLog = QTextEdit()
        self.eAlertLog.setReadOnly(True)
        self.eClearBtn = QPushButton("Clear Log")
        self.eClearBtn.clicked.connect(self.eAlertLog.clear)

        formLayot = QFormLayout()
        formLayot.addRow("Device ID", self.eDeviceID)
        formLayot.addRow("", self.eEnableCheck)
        formLayot.addRow("", self.eSoundCheck)
        formLayot.addRow("State", self.eStateLabel)
        formLayot.addRow("Alert Log", self.eAlertLog)
        formLayot.addRow("", self.eClearBtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Reed Event Handler")

    def check_reed_event(self, topic, payload_str):
        if not self.eEnableCheck.isChecked():
            return
        device_id = self.eDeviceID.text().strip()
        if device_id and device_id not in topic:
            return
        try:
            data = json.loads(payload_str)
        except Exception:
            return
        cname = str(data.get("cname", "")).upper()
        if cname not in ("REED", "BUTTON", "CONTACT"):
            return
        value = data.get("value", None)
        if value is None:
            return
        state = "OPEN" if value else "CLOSED"
        color = "red" if value else "green"
        self.eStateLabel.setText(f"Door: {state}")
        self.eStateLabel.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {color}; padding: 4px;"
        )
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.eAlertLog.append(f"[{ts}] {topic} → {state}")
        if self.eSoundCheck.isChecked():
            winsound.Beep(1000 if value else 500, 500)


class DeviceControlDock(QDockWidget):
    """Relay control — new for this assignment."""

    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc

        self.eTopicPrefix = QLineEdit("matzi/0/")
        self.eDeviceID = QLineEdit()
        self.eDeviceID.setPlaceholderText("e.g. 3PI_16168238")

        self.eRelayOn = QPushButton("Relay ON")
        self.eRelayOn.setStyleSheet("background-color: lightgreen; font-weight: bold")
        self.eRelayOn.clicked.connect(
            lambda: self.mc.relay_on(self.eTopicPrefix.text(), self.eDeviceID.text(), True)
        )
        self.eRelayOff = QPushButton("Relay OFF")
        self.eRelayOff.setStyleSheet("background-color: salmon; font-weight: bold")
        self.eRelayOff.clicked.connect(
            lambda: self.mc.relay_on(self.eTopicPrefix.text(), self.eDeviceID.text(), False)
        )

        formLayot = QFormLayout()
        formLayot.addRow("Topic Prefix", self.eTopicPrefix)
        formLayot.addRow("Device ID", self.eDeviceID)
        formLayot.addRow("", self.eRelayOn)
        formLayot.addRow("", self.eRelayOff)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Device Control")


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = Mqtt_client()

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 100, 900, 700)
        self.setWindowTitle('White Cubes GUI')

        # Init QDockWidget objects
        self.main          = MainDock(self.mc)
        self.publishDock   = PublishDock(self.mc)
        self.subscribeDock = SubscribeDock(self.mc)
        self.eventDock     = EventHandlerDock()
        self.controlDock   = DeviceControlDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea,    self.main)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.publishDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.subscribeDock)
        self.addDockWidget(Qt.RightDockWidgetArea,  self.eventDock)
        self.addDockWidget(Qt.RightDockWidgetArea,  self.controlDock)

        # All three signals run slots on the main thread via QueuedConnection,
        # so QTimer.start() and widget updates are always safe.
        self.mc.signals.message_received.connect(self._on_message, Qt.QueuedConnection)
        self.mc.signals.connected.connect(self.main.on_connected, Qt.QueuedConnection)
        self.mc.signals.disconnected.connect(self.main.on_disconnected, Qt.QueuedConnection)

    def _on_message(self, topic, payload):
        self.subscribeDock.update_mess_win(f"{topic}: {payload}")
        self.eventDock.check_reed_event(topic, payload)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
