
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
#from flask_cors import CORS
#from datetime import datetime, timedelta
import json
import paho.mqtt.client as mqtt
import requests
#import random

app = Flask(__name__)

#CORS(app, resources={r"/*": {"origins": "*"}})

url = "https://onesignal.com/api/v1/notifications"


ip_address = '10.4.174.147'

raspberry = []
jsonFile = open('raspberry.json', 'r')
raspberryJson = json.load(jsonFile)
for i in raspberryJson['raspberry']:
    raspberry.append(i)
showState = raspberryJson['show']
jsonFile.close()

def on_connectT(client, userdata, msg, rc):

    print("connected with result code " + str(rc))
    client.subscribe("topic/temp-humid")

def on_connectH(client, userdata, msg, rc):

    print("connected with result code " + str(rc))
    client.subscribe("topic/humo")

def on_connectM(client, userdata, msg, rc):

    print("connected with result code " + str(rc))
    client.subscribe("topic/mov")
    

def on_message(client, userdata, msg):
    json_body = json.loads(msg.payload.decode())
    payload = {
        "included_segments": ["Subscribed Users"],
        "contents":{
            "en": "Temperatura: " + str(json_body["temperatura"])  + "\nHumedad: " + str(json_body["humedad"])
        },
        "name": "NOTIFICATION TESTS",
        "app_id": "ccc3e0ea-e6e8-44d1-93db-4287eb8507a8"
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Basic MTAxNmY1ZDUtZTcxMS00NmZjLWJiYTMtZTc4ZDkzMmQ2MTRh",
        "content-type": "application/json"
    }

    requests.post(url, json=payload, headers=headers)


    client.disconnect()
    return postFeatures(json_body)

def getAll(scope):
    if scope == '':
        return jsonify(raspberry)
    elif scope == 'temperatura' or scope == 'humedad' or scope == 'humo' or scope == 'luz':
        subTiempo = [sub['tiempo'] for sub in raspberry]
        subFeature = [sub[scope] for sub in raspberry]

        feature = []
        for i in range(len(subFeature)):
             feature.append({
                'tiempo': subTiempo[i],
                scope: subFeature[i]
            })
        return jsonify(feature)

def postFeatures(req):
    raspberry.append(req)
    raspberryJson['raspberry'].append(req)
    jsonFile = open('raspberry.json', 'w+')
    jsonFile.write(json.dumps(raspberryJson))
    jsonFile.close()
    return 'Se agregó la información correctamente'

def changeShowState(show):
    global showState
    showState = show
    raspberryJson['show'] = show
    jsonFile = open('raspberry.json', 'w+')
    jsonFile.write(json.dumps(raspberryJson))
    jsonFile.close()
    return "Solicitud correcta. Status de Show cambiado."

@app.route('/',methods = ['GET','POST','PUT'])
def hello_world():
    if request.method == 'GET':
        if(showState):
            return getAll('')
        return []
    if request.method == 'POST':
        client = mqtt.Client()
        client.connect(ip_address)

        client.on_connect = on_connectT
        client.on_message = on_message

        client.loop_forever()

        return 'Se agregó la información correctamente'

    if request.method == 'PUT':
        return changeShowState(request.json['show'])
    

@app.route('/prenderLED', methods = ['GET'])
def LED():
    client = mqtt.Client()
    client.connect('localhost', 1883, 60)
    json_body = {"id": 1}
    res = json.dumps(json_body)

    client.publish("topic/actuador", res)
    client.disconnect()

    return json_body



@app.route('/prenderBuzzer', methods = ['GET'])
def Buzzer():
    client = mqtt.Client()
    client.connect('localhost', 1883, 60)
    json_body = {"id": 0}
    res = json.dumps(json_body)

    client.publish("topic/actuador", res)
    client.disconnect()

    return json_body

@app.route('/prenderServo', methods = ['GET'])
def Servo():
    client = mqtt.Client()
    client.connect('localhost', 1883, 60)
    json_body = {"id": 2}
    res = json.dumps(json_body)

    client.publish("topic/actuador", res)
    client.disconnect()

    return json_body
    
    
@app.route('/postTemperaturaHumedad',methods = ['POST'])
def postTempHum():

    client = mqtt.Client()
    client.connect(ip_address)

    client.on_connect = on_connectT
    client.on_message = on_message

    client.loop_forever()

    return 'Se agregó la información correctamente'

@app.route('/postHumo',methods = ['POST'])
def postHumo():

    client = mqtt.Client()
    client.connect(ip_address)

    client.on_connect = on_connectH
    client.on_message = on_message

    client.loop_forever()

    return 'Se agregó la información correctamente'

@app.route('/postMov',methods = ['POST'])
def postMov():

    client = mqtt.Client()
    client.connect(ip_address)

    client.on_connect = on_connectM
    client.on_message = on_message

    client.loop_forever()

    return 'Se agregó la información correctamente'


@app.route('/raspberry/features', methods = ['GET','POST','PUT'])
def raspberryFeatures():
    if request.method == 'GET':
        if(showState):
            return getAll('')
        return []
    if request.method == 'POST':
        return postFeatures(request)
    if request.method == 'PUT':
        return changeShowState(request.json['show'])

@app.route('/raspberry/features/temperatura', methods = ['GET'])
def temperaturas():
    global showState
    if(showState):
        return getAll('temperatura')
    return []

@app.route('/raspberry/features/humedad', methods = ['GET'])
def humedades():
    global showState
    if(showState):
        return getAll('humedad')
    return []

@app.route('/raspberry/features/humo', methods = ['GET'])
def humos():
    global showState
    if(showState):
        return getAll('humo')
    return []

@app.route('/raspberry/features/luz', methods = ['GET'])
def luces():
    global showState
    if(showState):
        return getAll('luz')
    return []

app.run(debug=True, port=8080)