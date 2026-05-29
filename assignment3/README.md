# IoT Assignment 3 — PyQt5 MQTT GUI App

PyQt5-based GUI application for monitoring and controlling White Cube IoT devices over MQTT.

---

## Project Structure

```
assignment3/
├── src/
│   ├── white_cube_app.py     # Main submission app (full-featured GUI)
│   ├── MonitorGUI.py         # Basic monitor GUI (earlier version)
│   └── mqtt_init.py          # Broker config (HiveMQ / HIT server)
├── GUI_Template/             # Professor's reference template
│   ├── cubes_gui_main_template.py
│   ├── example_connect.py
│   ├── gui_helpers.py
│   ├── gui_main.py
│   ├── IoT_MQ_main.py
│   └── icons/
├── docs/
│   └── Assignment3_Yakira_Siboni.pdf
└── outputs/
    └── presentation.gif
```

---

## Prerequisites

- Python 3.8+
- Internet access (connects to `broker.hivemq.com:1883`)

---

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:Yakira3012/iot-course.git
cd iot-course/assignment3
```

### 2. Install dependencies

```bash
pip install paho-mqtt PyQt5
```

---

## Running

```bash
cd src
python white_cube_app.py
```

The GUI opens with five dockable panels:

| Panel | Description |
|---|---|
| Connection | Set broker host, port, client ID, credentials, run time; connect/disconnect with live status indicator |
| Publish | Publish a message to any topic with configurable QoS and retain flag |
| Subscribe | Subscribe/unsubscribe to any topic; displays incoming messages |
| Reed Event Handler | Monitors Reed sensor events — shows door OPEN/CLOSED state, logs alerts, triggers sound alarm |
| Device Control | Send Relay ON/OFF commands to a specific device ID |

---

## Broker Configuration

Configured in `src/mqtt_init.py`:

| Setting | Value |
|---|---|
| Broker | `broker.hivemq.com` |
| Port | `1883` |
| Credentials | none (public broker) |

Set `nb = 0` to switch to the HIT private server (`vmm1.saaintertrade.com:80`, credentials: `MATZI/MATZI`).
