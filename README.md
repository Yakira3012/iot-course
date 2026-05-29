# Software Development for IoT in Smart City Environment

**Author:** Yakira Siboni

A hands-on IoT course covering communication protocols, embedded systems, cloud platforms, and smart city application development. Topics include MQTT, TCP/IP, REST services, PyQt5 GUI development, IaaS cloud, and data analytics.

---

## Assignments

- [Assignment 1 — MQTT Publisher & Subscriber](./assignment1/README.md)
- [Assignment 2 — MQTT HiveMQ IoT Control](./assignment2/README.md)
- [Assignment 3 — PyQt5 MQTT GUI App](./assignment3/README.md)
- [Assignment 4 — ThingsBoard Hello World](./assignment4/README.md)

---

## What Was Built

**Assignment 1** — Explored the MQTT protocol fundamentals by implementing a publisher and subscriber in Python using `paho-mqtt`. Ran 5 tests varying `clean_session` and QoS levels (0 and 1) to observe how the HiveMQ broker handles message retention, session persistence, and delivery guarantees. Documented results in a summary table.

**Assignment 2** — Built an event-driven IoT control system using PyQt5 device emulators (DHT sensor, Relay, Push Button) connected to the HiveMQ public broker. Implemented three tests: continuous DHT temperature/humidity data collection exported to a formatted Excel file with charts; remote Relay ON/OFF control via MQTT publish commands; and a Button-triggered Relay toggle using an event handler that reacts to incoming MQTT messages in real time.

**Assignment 3** — Developed a full-featured PyQt5 desktop GUI application for monitoring and controlling White Cube IoT devices. The app includes configurable broker connection settings, a real-time message subscribe/publish interface, a Reed sensor event handler with sound alarm and alert log, a Relay device control panel, and a live connection status indicator with auto-disconnect timer.

**Assignment 4** — Completed the ThingsBoard Cloud Hello World quickstart. Provisioned a virtual Thermometer device, pushed telemetry via HTTP, and built a real-time dashboard with a value card, time series chart, and alarms table. Defined a Critical alarm rule triggered when temperature exceeds 25°C, verified it fires correctly, then set up a customer tenant with a limited-role user account to demonstrate multi-tenant access control.
