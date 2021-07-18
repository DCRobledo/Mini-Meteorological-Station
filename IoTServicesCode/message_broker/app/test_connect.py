import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fall with code", {rc})

client = mqtt.Client()
client.username_pw_set(username="Omg", password="Omg")
client.on_connect = on_connect
client.connect("Imagine if there is an IP here", 1883, 60)
client.loop_forever()
