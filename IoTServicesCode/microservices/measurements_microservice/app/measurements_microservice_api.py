import os
import json
from flask import Flask, request
from flask_cors import CORS

from measurements_microservice import *

app = Flask(__name__)
CORS(app)

@app.route('/measurements/register', methods=['POST'])
def set_measurement():
    params = request.get_json()
    measurements_register(params)
    return {"result":"record inserted"}, 201

@app.route('/measurements/retrieve/')
def get_measurements():
    return measurements_retriever()

@app.route('/measurements/retrieve_interval/')
def get_measurements_on_interval():
    params = request.get_json()
    params["start_date"] = params["start_date"].replace("-", "/")
    params["end_date"] = params["end_date"].replace("-", "/")
    return measurements_interval_retriever(params)

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
app.run(host = HOST, port = PORT)
