import requests
import os

def submit_data_to_store (data):
    host = os.getenv("MEASUREMENTS_MICROSERVICE_ADDRESS")
    port = os.getenv("MEASUREMENTS_MICROSERVICE_PORT")
    r = requests.post('http://' + host + ':' + port + '/measurements/register', json=data)