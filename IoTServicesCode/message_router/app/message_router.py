import paho.mqtt.client as paho
import os

from measurement_register_interface import *
from device_register_interface import *


myhost = os.getenv("BROKER_ADDRESS")
myport = int(os.getenv("BROKER_PORT"))
myuser = os.getenv("BROKER_USER")
mypassword = os.getenv("BROKER_PWD")
mykeepalive = int(os.getenv("BROKER_KEEP_ALIVE"))

current_temperature = 0
current_humidity = 0
current_timestamp = 0

current_device_id = 0
current_device_state = 0
current_device_location = 0
current_device_timestamp = 0


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected success")
        client.subscribe("temperature")
        client.subscribe("humidity")
        client.subscribe("timestamp")
        client.subscribe("device_id")
        client.subscribe("device_state")
        client.subscribe("device_location")
        client.subscribe("device_timestamp")
    else:
        print("Connected fail with code", {rc})

def on_message(client, userdata, message):
    global current_temperature, current_humidity, current_timestamp, current_device_id, current_device_state, current_device_location, current_device_timestamp
    
    print("received message =",str(message.payload.decode("utf-8")))
    
    
    if message.topic == "temperature":
        current_temperature = float(message.payload.decode("utf-8"))
        data = {"temperature": current_temperature, "humidity": current_humidity, "timestamp": current_timestamp}
        submit_data_to_store(data)
        print(data)
        
    if message.topic == "humidity":
        current_humidity = float(message.payload.decode("utf-8"))
        data = {"temperature": current_temperature, "humidity": current_humidity, "timestamp": current_timestamp}
        submit_data_to_store(data)
        print(data)
        
    if message.topic == "timestamp":
        current_timestamp = message.payload.decode("utf-8")
        data = {"temperature": current_temperature, "humidity": current_humidity, "timestamp": current_timestamp}
        submit_data_to_store(data)
        print(data)
        
        
    if message.topic == "device_id":
        current_device_id = message.payload.decode("utf-8")
        data = {"device_id": current_device_id, "device_state": current_device_state, "device_location": current_device_location, "device_timestamp": current_device_timestamp}
        submit_device_info_to_store(data)
        print(data)
        
    if message.topic == "device_state":
        current_device_state = message.payload.decode("utf-8")
        data = {"device_id": current_device_id, "device_state": current_device_state, "device_location": current_device_location, "device_timestamp": current_device_timestamp}
        submit_device_info_to_store(data)
        print(data)
        
    if message.topic == "device_location":
        current_device_location = message.payload.decode("utf-8")
        data = {"device_id": current_device_id, "device_state": current_device_state, "device_location": current_device_location, "device_timestamp": current_device_timestamp}
        submit_device_info_to_store(data)
        print(data)
        
    if message.topic == "device_timestamp":
        current_device_timestamp = message.payload.decode("utf-8")
        data = {"device_id": current_device_id, "device_state": current_device_state, "device_location": current_device_location, "device_timestamp": current_device_timestamp}
        submit_device_info_to_store(data)
        print(data)
        
        
client = paho.Client()
client.username_pw_set(username=myuser, password=mypassword)

client.on_connect = on_connect

client.on_message=on_message

print("connecting to broker", myhost)

client.connect(myhost, myport, mykeepalive)
client.loop_forever()
