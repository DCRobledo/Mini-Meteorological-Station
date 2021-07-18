import os
from flask import Flask, request
from flask_cors import CORS

from devices_microservice import *

app = Flask(__name__)
CORS(app)

@app.route('/devices/register', methods=['POST'])
def set_device():
    params = request.get_json()
    devices_register(params)
    return {"result":"record inserted"}, 201

@app.route('/devices/retrieve/')
def get_devices():
    return devices_retriever()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
app.run(host = HOST, port = PORT)
