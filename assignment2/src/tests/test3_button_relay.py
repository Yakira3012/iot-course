import sys
import paho.mqtt.client as mqtt
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from mqtt_init import *

# Student: Yakira Siboni, ID: 208499426
# Run: python test3_button_relay.py pr/home/<TOPIC>/sts
# (topic is printed by RELAY.py on startup as "[RELAY] Topic: ...")
BUTTON_TOPIC = 'pr/home/button_123_YY/sts'  # matches BUTTON.py
RELAY_TOPIC  = sys.argv[1] if len(sys.argv) > 1 else 'pr/home/YOUR_RELAY_TOPIC_HERE/sts'
if 'YOUR_RELAY_TOPIC_HERE' in RELAY_TOPIC:
    print("ERROR: pass relay topic as argument: python test3_button_relay.py <topic>")
    sys.exit(1)

CMD_ON  = '{"type":"set_state","action":"set_value","addr":0,"cname":"ONOFF","value":1}'
CMD_OFF = '{"type":"set_state","action":"set_value","addr":0,"cname":"ONOFF","value":0}'

relay_state = False  # Track current relay state (False=OFF, True=ON)

def on_log(client, userdata, level, buf):
    print("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
        client.subscribe(BUTTON_TOPIC, qos=0)
        client.subscribe(RELAY_TOPIC, qos=0)
        print(f"Subscribed to BUTTON: {BUTTON_TOPIC}")
        print(f"Subscribed to RELAY:  {RELAY_TOPIC}")
        print("\nWaiting for button events... (Press PUSH BUTTON in the emulator)\n")
    else:
        print("Bad connection, code =", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected, code =", str(rc))

def on_message(client, userdata, msg):
    global relay_state
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))

    if topic == BUTTON_TOPIC:
        # Button event detected — toggle relay
        print(f"[BUTTON EVENT] {m_decode}")
        relay_state = not relay_state
        cmd = CMD_ON if relay_state else CMD_OFF
        state_str = "ON" if relay_state else "OFF"
        client.publish(RELAY_TOPIC, cmd)
        print(f"  -> Toggling RELAY to {state_str}")

    elif topic == RELAY_TOPIC:
        # Relay status update
        print(f"[RELAY STATUS] {m_decode}")

import random
r = random.randrange(1, 10000000)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, f"IOT_btn_relay_{r}", clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username, password)

print(f"Connecting to broker {broker_ip}:{broker_port}")
client.connect(broker_ip, int(broker_port))
client.loop_start()

# Run for 5 minutes — push the button in the emulator during this time
try:
    print("Running for 5 minutes. Press Ctrl+C to stop early.\n")
    time.sleep(300)
except KeyboardInterrupt:
    print("\nStopped by user.")

client.loop_stop()
client.disconnect()
print("Test 3 complete.")
