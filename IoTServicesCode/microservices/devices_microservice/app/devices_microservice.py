import os
import mysql.connector
import json
from datetime import datetime

def connect_database():
    mydb = mysql.connector.connect(host=os.getenv('DBHOST'), user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD'), database=os.getenv('DBDATABASE'))
    return mydb

def devices_retriever():
    mydb = connect_database()
    
    r = {}
    
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT device_id, device_state, device_location, device_timestamp FROM devices ORDER BY id DESC;")
        
        myresult = mycursor.fetchall()

        i = 0
        
        for device_id, device_state, device_location, device_timestamp in myresult:
            r[i] = {"device_id": device_id, "device_state": device_state, "device_location": device_location, "device_timestamp": device_timestamp.strftime("%Y/%d/%m %H:%M:%S")}
            i += 1

        mydb.commit()

    return r

def devices_register(params):
    mydb = connect_database()
    
    timestamp = datetime.strptime(params["device_timestamp"], '%Y/%d/%m %H:%M:%S')
    
    with mydb.cursor() as mycursor:
        
        sql = "INSERT INTO devices (device_id, device_state, device_location, device_timestamp) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE device_state=%s,device_location=%s, device_timestamp=%s"
        val = (params["device_id"], params["device_state"], params["device_location"], timestamp, params["device_state"], params["device_location"], timestamp)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
