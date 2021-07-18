import mysql.connector
import os
import json
from datetime import datetime


def connect_database():
    mydb = mysql.connector.connect(host=os.getenv('DBHOST'), user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD'), database=os.getenv('DBDATABASE'))
    return mydb


def measurements_retriever():
    mydb = connect_database()
    
    r = {}
    
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT temperature, humidity, timestamp FROM measurements ORDER BY id DESC;")
        
        myresult = mycursor.fetchall()
        
        i = 0
        
        for temperature, humidity, timestamp in myresult:
            r[i] = {"temperature": temperature, "humidity": humidity, "timestamp": timestamp.strftime("%Y/%d/%m %H:%M:%S")}
            i += 1
            
        mydb.commit()
    
    return r

def measurements_interval_retriever(params):
    mydb = connect_database()
    
    r = {}
    
    start_date, end_date = (datetime.strptime(params["start_date"], '%Y/%m/%d %H:%M:%S'), datetime.strptime(params["end_date"], '%Y/%m/%d %H:%M:%S'))
    
    with mydb.cursor() as mycursor:
        sql = "SELECT temperature, humidity, timestamp FROM measurements WHERE timestamp BETWEEN %s AND %s ORDER BY id DESC;"
        val = (start_date, end_date)
        mycursor.execute(sql, val)
        
        myresult = mycursor.fetchall()
        
        i = 0
        
        for temperature, humidity, timestamp in myresult:
            r[i] = {"temperature": temperature, "humidity": humidity, "timestamp": timestamp.strftime("%Y/%d/%m %H:%M:%S")}
            i += 1
            
        mydb.commit()
    
    return r

def measurements_register(params):
    mydb = connect_database()
    
    timestamp = datetime.strptime(params["timestamp"], '%Y/%d/%m %H:%M:%S')
    
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO measurements (temperature, humidity, timestamp) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE temperature = %s, humidity = %s"
        val = (params["temperature"], params["humidity"], timestamp, params["temperature"], params["humidity"])
        mycursor.execute(sql, val)
        
        mydb.commit()
        
        print(mycursor.rowcount, "record inserted")