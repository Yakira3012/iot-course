# IoT Assignment 2 — MQTT HiveMQ Communication

MQTT-based IoT assignment using HiveMQ public broker and PyQt5 device emulators. Implements three tests: DHT data collection, Relay control, and Button-triggered Relay toggling.

---

## Project Structure

```
assignment2/
├── src/
│   ├── modules/                  # Shared modules
│   │   ├── mqtt_init.py          # Broker config (HiveMQ, topics, credentials)
│   │   ├── DHT.py                # DHT sensor emulator (PyQt5 GUI)
│   │   ├── RELAY.py              # Relay emulator (PyQt5 GUI)
│   │   └── BUTTON.py             # Push-button emulator (PyQt5 GUI)
│   ├── tests/                    # Test scripts
│   │   ├── test1_dht_collector.py   # Test 1: collect 20 DHT samples → Excel
│   │   ├── test2_relay_control.py   # Test 2: send ON/OFF commands to Relay
│   │   └── test3_button_relay.py    # Test 3: toggle Relay on Button press
│   └── cubes_test.py             # Base template / example script
├── data/
│   └── dht_data_yakira_siboni.xlsx  # Output from Test 1
├── docs/
│   └── Assignment2_Report_Yakira_Siboni_208499426.pdf
└── outputs/
    ├── test2_output.gif
    └── test3_output.gif
```

---

## Prerequisites

- Python 3.8+
- Internet access (connects to public HiveMQ broker: `broker.hivemq.com:1883`)

---

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:Yakira3012/iot-course.git
cd iot-course/assignment2
```

### 2. Install dependencies

```bash
pip install paho-mqtt PyQt5 openpyxl
```

---

## Running the Tests

All test scripts and emulators import from `src/modules/`, so **run every command from the `src/` directory**:

```bash
cd src
```

---

### Test 1 — DHT Data Collection

**Goal:** Subscribe to the DHT emulator topic, collect 20 temperature/humidity samples, and export them to an Excel file.

**Step 1 — Start the DHT emulator** (opens a PyQt5 GUI window):
```bash
python modules/DHT.py
```
In the GUI, click **Enable/Connect**. The emulator will begin publishing readings every 5 seconds.

**Step 2 — Run the collector** (in a separate terminal from `src/`):
```bash
python tests/test1_dht_collector.py
```
The script subscribes to `pr/home/5976397/sts`, collects 20 samples (~10 minutes), then saves `dht_data_yakira_siboni.xlsx` and exits.

---

### Test 2 — Relay Control

**Goal:** Send ON and OFF commands to the Relay emulator and observe state changes.

**Step 1 — Start the Relay emulator**:
```bash
python modules/RELAY.py
```
On startup it prints its unique topic, e.g.:
```
[RELAY] Topic: pr/home/3847291/sts
```
Copy that topic string — you need it in the next step.

**Step 2 — Run the relay control script**:
```bash
python tests/test2_relay_control.py pr/home/<YOUR_RELAY_TOPIC>/sts
```
The script sends ON → OFF → ON → OFF with 5-second pauses between each command. Watch the Status button in the RELAY GUI change color.

---

### Test 3 — Button triggers Relay

**Goal:** Every time the push button is pressed, the Relay toggles state.

**Step 1 — Start both emulators** (each in its own terminal from `src/`):
```bash
python modules/RELAY.py   # note the printed topic
python modules/BUTTON.py
```

**Step 2 — Run the event handler**:
```bash
python tests/test3_button_relay.py pr/home/<YOUR_RELAY_TOPIC>/sts
```
The script runs for 5 minutes. Click **PUSH BUTTON** in the BUTTON GUI — the Relay toggles ON/OFF with each press. Press `Ctrl+C` to stop early.

---

## Broker Configuration

Configured in `src/modules/mqtt_init.py`:

| Setting | Value |
|---|---|
| Broker | `broker.hivemq.com` |
| Port | `1883` |
| Credentials | none (public broker) |
| Subscribe topic | `#` (all) |

To switch to a private broker, set `nb = 0` in `mqtt_init.py` and update credentials.

---

## Monitor via Browser

You can monitor all MQTT traffic in a browser at:
`http://www.hivemq.com/demos/websocket-client/`

Connect to `broker.hivemq.com:8000` and subscribe to `#` to see all messages.
