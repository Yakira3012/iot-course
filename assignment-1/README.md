# IoT Assignment 1 — MQTT Publisher & Subscriber

Basic MQTT assignment exploring the effect of `clean_session` and QoS levels on message delivery, using the public HiveMQ broker.

---

## Project Structure

```
assignment-1/
├── src/
│   ├── mqtt_publisher_client_modified.py   # Publisher: sends retained message with Last Will
│   └── mqtt_subscriber_client_modified.py  # Subscriber: listens on sensor topic for 10 sec
├── docs/
│   ├── Assignment1_Yakira_Siboni_208499426.pdf   # Full report with screenshots & analysis
│   └── Summary.xlsx                              # QoS / clean_session results table
└── screenshots/
    ├── code/
    │   ├── publisher-code.png
    │   └── subscriber-code.png
    └── tests/
        ├── test1-publisher.png / test1-subscriber.png
        ├── test2-publisher.png / test2-subscriber.png
        ├── test3-publisher.png / test3-subscriber.png
        ├── test4-publisher.png / test4-subscriber.png
        └── test5-publisher.png / test5-subscriber.png
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
cd iot-course/assignment-1
```

### 2. Install dependencies

```bash
pip install paho-mqtt
```

---

## Running

Both scripts connect to `broker.hivemq.com:1883` with `keepalive=90s`. Run from the `src/` directory.

```bash
cd src
```

**Publisher** — connects, publishes one retained message, then disconnects:
```bash
python mqtt_publisher_client_modified.py
```

**Subscriber** — connects, subscribes to the sensor topic with QoS 1, listens for 10 seconds, then disconnects:
```bash
python mqtt_subscriber_client_modified.py
```

Run the subscriber first (or in a separate terminal), then the publisher, to observe message delivery.

---

## Test Matrix

Each test varies `clean_session` and QoS to observe broker behaviour. Modify the values in both scripts before each run.

| Test | `clean_session` | Pub QoS | Sub QoS | Expected result |
|------|----------------|---------|---------|-----------------|
| 1 | `True` | 0 | 0 | No messages received after reconnect |
| 2 | `False` | 0 | 0 | Messages received (broker remembers subscription) |
| 3 | `True` | 1 | 1 | No messages received after reconnect |
| 4 | `False` | 1 | 1 | Messages received after reconnect |
| 5 | `False` | 0 | 1 | No messages received (pub QoS must also be > 0) |

See `docs/Summary.xlsx` for the full results table and `docs/Assignment1_Yakira_Siboni_208499426.pdf` for the detailed analysis.

---

## MQTT Configuration

| Setting | Value |
|---|---|
| Broker | `broker.hivemq.com` |
| Port | `1883` |
| Topic | `iot/home_YY/sensor_9426` |
| Keep Alive | 90 sec |
| Last Will topic | `iot/home_YY/sensor_9426` |
| Last Will payload | `Publisher disconnected unexpectedly` |

---

## Monitor via Browser

You can monitor messages in real time at:
`http://www.hivemq.com/demos/websocket-client/`

Connect to `broker.hivemq.com` (port 8000, WebSocket) and subscribe to `iot/home_YY/#`.
