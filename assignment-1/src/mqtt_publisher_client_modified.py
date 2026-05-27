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
        print("message received",m_decode)

# Student: Yakira Siboni, ID: 208499426
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "IoT_YY_9426", clean_session=False)  # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message

# Last Will message - sent by broker if client disconnects unexpectedly
client.will_set("iot/home_YY/sensor_9426", payload="Publisher disconnected unexpectedly", qos=0, retain=False)

print("Connecting to broker ", broker)
port=1883
# keepalive set to 90 seconds as required
client.connect(broker, port, keepalive=90)

pub_topic = "iot/home_YY/sensor_9426"

# Publish a retained message to the topic
client.publish(pub_topic, "my 'retained' test message - Yakira Siboni 208499426", 0, True)

time.sleep(1)

print("End publish_client run script")

client.disconnect()  # disconnect
