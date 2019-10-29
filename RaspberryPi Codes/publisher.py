import paho.mqtt.client as mqtt
import sys
# This is the Publisher

rfid = str(sys.argv[1])
client = mqtt.Client()
client.connect("192.168.137.197",1883,60)

client.publish("inTopic","uploaded");
client.publish("rfid",rfid)
print("MQTT : ",rfid)
client.disconnect();
