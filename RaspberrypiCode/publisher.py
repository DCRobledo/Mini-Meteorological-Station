import paho.mqtt.client as mqtt
import time
from datetime import datetime

def on_connect(client, userdate, flags, rc):
    if rc == 0:
        print("Connect success")
    else:
        print("Connect fail with code", {rc})
        
client = mqtt.Client()

def make_connection():
    client.username_pw_set(username="Have a nice day! :D", password="Have a nice day! :D")

    client.on_connect = on_connect
    
    client.will_set('device_state', payload="OFF")
    client.will_set('device_timestamp', payload=datetime.now().strftime("%Y/%d/%m %H:%M:%S"))
    
    client.connect("34.78.224.246", 1883, 60)
    
def disconnect():
    client.disconnect()
    
def send_measurement(temperature, humidity, timestamp):
    client.publish('temperature', payload=temperature, qos=0, retain=False)
    client.publish('humidity', payload=humidity, qos=0, retain=False)
    client.publish('timestamp', payload=timestamp, qos=0, retain=False)
    
    time.sleep(1)
    
def send_device_info(device_id, device_state, device_location, device_timestamp):
    client.publish('device_id', payload=device_id, qos=0, retain=False)
    client.publish('device_state', payload=device_state, qos=0, retain=False)
    client.publish('device_location', payload=device_location, qos=0, retain=False)
    client.publish('device_timestamp', payload=device_timestamp, qos=0, retain=False)
    
    time.sleep(1)
