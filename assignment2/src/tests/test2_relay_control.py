import sys
import paho.mqtt.client as mqtt
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from mqtt_init import *

# Student: Yakira Siboni, ID: 208499426
# Run: python test2_relay_control.py pr/home/<TOPIC>/sts
# (topic is printed by RELAY.py on startup as "[RELAY] Topic: ...")
RELAY_TOPIC = sys.argv[1] if len(sys.argv) > 1 else 'pr/home/YOUR_RELAY_TOPIC_HERE/sts'
if 'YOUR_RELAY_TOPIC_HERE' in RELAY_TOPIC:
    print("ERROR: pass relay topic as argument: python test2_relay_control.py <topic>")
    sys.exit(1)

CMD_ON  = '{"type":"set_state","action":"set_value","addr":0,"cname":"ONOFF","value":1}'
CMD_OFF = '{"type":"set_state","action":"set_value","addr":0,"cname":"ONOFF","value":0}'

def on_log(client, userdata, level, buf):
    print("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
        client.subscribe(RELAY_TOPIC, qos=0)
        print(f"Subscribed to: {RELAY_TOPIC}")
    else:
        print("Bad connection, code =", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected, code =", str(rc))

def on_message(client, userdata, msg):
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print(f"[RELAY STATUS] {m_decode}")

import random
r = random.randrange(1, 10000000)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, f"IOT_relay_ctrl_{r}", clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username, password)

print(f"Connecting to broker {broker_ip}:{broker_port}")
client.connect(broker_ip, int(broker_port))
client.loop_start()
time.sleep(2)  # Wait for connection

print("\n--- Sending ON command ---")
client.publish(RELAY_TOPIC, CMD_ON)
print(f"Published ON to {RELAY_TOPIC}")
time.sleep(5)  # Observe ON state

print("\n--- Sending OFF command ---")
client.publish(RELAY_TOPIC, CMD_OFF)
print(f"Published OFF to {RELAY_TOPIC}")
time.sleep(5)  # Observe OFF state

print("\n--- Sending ON command again ---")
client.publish(RELAY_TOPIC, CMD_ON)
print(f"Published ON to {RELAY_TOPIC}")
time.sleep(5)

print("\n--- Sending OFF command again ---")
client.publish(RELAY_TOPIC, CMD_OFF)
print(f"Published OFF to {RELAY_TOPIC}")
time.sleep(3)

client.loop_stop()
client.disconnect()
print("\nTest 2 complete.")
