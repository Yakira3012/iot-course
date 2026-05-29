import paho.mqtt.client as mqtt  #import the client1
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# broker list
brokers=["iot.eclipse.org","broker.hivemq.com",\
         "test.mosquitto.org","192.168.8.167","139.162.222.115"]

broker=brokers[1]


def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
def on_message(client,userdata,msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("Message Topic: ", topic)
        print("message received: ", m_decode)

# Student: Yakira Siboni, ID: 208499426
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "IoT_sub_YY_9426", clean_session=False)  # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message

print("Connecting to broker ", broker)
port=1883
# keepalive set to 90 seconds as required
client.connect(broker, port, keepalive=90)

sub_topic = 'iot/home_YY/sensor_9426'

client.loop_start()   # Start loop
client.subscribe(sub_topic, qos=1)

time.sleep(10)
client.loop_stop()    # Stop loop
client.disconnect()
