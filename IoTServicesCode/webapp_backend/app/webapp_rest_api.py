from flask import Flask
from flask_cors import CORS
from flask import request
import requests
import os

myhost = os.getenv("HOST")
myport = int(os.getenv("PORT"))
measurements_host = os.getenv("MEASUREMENTS_MICROSERVICE_ADDRESS")
measurements_port = os.getenv("MEASUREMENTS_MICROSERVICE_PORT")
devices_host = os.getenv("DEVICES_MICROSERVICE_ADDRESS")
devices_port = os.getenv("DEVICES_MICROSERVICE_PORT")


app = Flask(__name__)
CORS(app)

@app.route('/dso/measurements/')
def get_sensor_data():
    response = requests.get('http://' + measurements_host + ":" + str(measurements_port) + '/measurements/retrieve/')
    return response.content

@app.route('/dso/measurements_interval')
def get_measurements_on_interval():
    params = {"start_date": request.args.get("start_date"), "end_date": request.args.get("end_date")}
    response = requests.get('http://' + measurements_host + ":" + str(measurements_port) + '/measurements/retrieve_interval/', json=params)
    return response.content

@app.route('/dso/devices/')
def get_devices_list():
    response = requests.get('http://' + devices_host + ":" + str(devices_port) + '/devices/retrieve/', headers={'Content-type': 'application/json'})
    return response.content

app.run(host=myhost, port=myport)
