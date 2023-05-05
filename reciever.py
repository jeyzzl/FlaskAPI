import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('topic/temp-humid')

def on_message(client, userdata, msg):
    res = json.dumps(msg.payload.decode())

    print(res)
    client.disconnect()

client = mqtt.Client()
client.connect('10.15.143.64', 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()