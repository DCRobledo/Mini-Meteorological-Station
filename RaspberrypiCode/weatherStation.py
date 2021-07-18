import sys
import time
import threading
import uuid
from datetime import datetime

import Adafruit_DHT
import RPi.GPIO as GPIO
import serial
import pynmea2
import signal

import RaspberrypiCode.lcd_lib

from RaspberrypiCode.publisher import *


# -------------------------------------------------------
# -------------- VARIABLES' DECLARATIONS ----------------
# -------------------------------------------------------

should_measure_temperature = True

global last_temperature
last_temperature = 0

global last_minute
last_minute = 0

global last_hour
last_hour = 0

global device_id
device_id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])

global device_location
device_location = None

global threads
threads = []

global is_finished
is_finished = False

exit_event = threading.Event()

# -------------------------------------------------------
# ------------------ GPS INCLUSION ----------------------
# -------------------------------------------------------

mport = "/dev/serial0"

ser = serial.Serial(mport,9600 ,timeout = 2)

def get_GPS_location():
    while True:
        try:
            str = ser.readline().decode()
            if str.find('GGA') > 0:
                msg = pynmea2.parse(str)
                device_location = ("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.num_sats))
        except:
            continue


# -------------------------------------------------------
# ----------------- LCD REPRESENTATION ------------------
# -------------------------------------------------------
global lcd
lcd = None
lcd = RaspberrypiCode.lcd_lib.lcd()
lcd.lcd_write(RaspberrypiCode.lcd_lib.LCD_CLEARDISPLAY)

def show_measure(measure):
    lcd.lcd_clear()
    
    lcd_line_1 = "Default message"
    lcd_line_2 = "Default message"
    
    if(should_measure_temperature):
        lcd_line_1 = "Showing temp" if measure is not None else "Sensore failure"
        lcd_line_2 = "Temp = " + str(measure) + "C" if measure is not None else "Temp = Undefined" 
    else:
        lcd_line_1 = "Showing humidity" if measure is not None else "Sensore failure"
        lcd_line_2 = "Humidity = " + str(measure) + "%" if measure is not None else "Humidity = Undefined" 

    lcd.lcd_display_string(lcd_line_1, 1)
    lcd.lcd_display_string(lcd_line_2, 2)
        
# -------------------------------------------------------
# --------------- BUTTON FUNCTIONALITY ------------------
# -------------------------------------------------------

button_gpio = 16

def signal_handler(sig, frame):

    exit_event.set()
    for t in threads:
        t.join()

    GPIO.cleanup()
    lcd.lcd_clear()
    
    device_id, device_state, device_location, device_timestamp = get_device_info()
    send_device_info(device_id, "OFF", device_location, datetime.now().strftime("%Y/%d/%m %H:%M:%S"))
    
    disconnect()
    
    sys.exit(0)

def button_pressed_callback(channel):
    lcd.lcd_clear()
    global should_measure_temperature
    should_measure_temperature = not should_measure_temperature
        
        
        
# -------------------------------------------------------
# ---------------- DEVICES MICROSERVICE -----------------
# -------------------------------------------------------
def get_device_info(): 
    #device_location = get_GPS_location()
    device_location = "myLocation"
    device_state = "ON"
    device_timestamp = datetime.now().strftime("%Y/%d/%m %H:%M:%S")
    
    return device_id, device_state, device_location, device_timestamp

def devices_microservice():
    # First device info record
    device_id, device_state, device_location, device_timestamp = get_device_info()
    
    send_device_info(device_id, device_state, device_location, device_timestamp)
    
    last_hour = int(datetime.now().strftime("%H"))
    
    print("FIRST DEVICE INFO ->" "id = " + str(device_id) + " state = " + str(device_state) + " location = " + str(device_location) + " time =" + str(device_timestamp))
    
    # Main loop
    while True:
        current_hour = int(datetime.now().strftime("%H"))
        
        # If the hour has changed, we send the new device information
        if current_hour != last_hour:
            device_id, device_location, device_timestamp = get_device_info()
            
            print("DEVICE INFO ->" "id = " + str(device_id) + " state = " + str(device_state) + " location = " + str(device_location) + " time =" + str(device_timestamp))

            send_device_info(device_id, device_location, device_timestamp)

        if(exit_event.is_set()):
            print("Device microservice ended")
            break
                        
        time.sleep(2) 


# -------------------------------------------------------
# ------------- MEASUREMENTS MICROSERVICE ---------------
# -------------------------------------------------------

def measure_environment():
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    
    temperature, humidity = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    return humidity, temperature

def get_measurement():
    # Measure both temperature and humidity
    temperature, humidity = measure_environment()
    
    # Record the timestamp
    timestamp = datetime.now().strftime("%Y/%d/%m %H:%M:%S")
    
    return temperature, humidity, timestamp

def measurements_microservice():
    # First measurement info record
    temperature, humidity, timestamp = get_measurement()
    
    # Show the measure on the lcd display
    if(should_measure_temperature):
        show_measure(temperature)
    else:
        show_measure(humidity)
        
    if (temperature is not None and humidity is not None):
        send_measurement(temperature, humidity, timestamp)
    
    # We need to track the starting temperature and the first minute in order to implement the correct intervals
    last_temperature = temperature
    last_minute = int(datetime.now().strftime("%M"))
    
    print("FIRST MEASURE INFO ->" + " temperature= " + str(temperature) + " humidity= " + str(humidity) + " timestamp= " + str(timestamp))
    
    # Main loop
    while True:
        # Get the measurement information
        temperature, humidity, timestamp = get_measurement()
        
        
        # Show the measure on the lcd display
        if(should_measure_temperature):
            show_measure(temperature)
        else:
            show_measure(humidity)
        
        
        # Check the minute we are currently at
        current_minute = int(datetime.now().strftime("%M"))
        
        
        # If the temperature has changed or if is has past a minute, we send the new measurement information
        if (temperature is not None and humidity is not None) and (last_minute != current_minute or last_temperature != temperature):
            send_measurement(temperature, humidity, timestamp)
            
            print("MEASURE INFO -> " + "temperature= " + str(temperature) + " humidity= " + str(humidity) + " timestamp= " + str(timestamp))
            
            # We update both the last temperature and last minute only if they have changed
            last_temperature = temperature if last_temperature != temperature else last_temperature
            last_minute = current_minute if last_minute != current_minute else last_minute
            
        if(exit_event.is_set()):
            print("Measurements microservice ended")
            break
            
        time.sleep(2) 
 
 
 
# -------------------------------------------------------
# ------------------ MAIN FUNCTION ----------------------
# -------------------------------------------------------        

if __name__ == "__main__":
    # Set up device's configuration
    GPIO.setmode(GPIO.BCM)
    
    # Set up button
    GPIO.setup(button_gpio, GPIO.IN, pull_up_down = (GPIO.PUD_UP))
    GPIO.add_event_detect(button_gpio, GPIO.RISING, callback=button_pressed_callback, bouncetime=200)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Make the connection
    make_connection()
    
    # Thread management
    try:
        mThread = threading.Thread(name="mThread", target=measurements_microservice)
        threads.append(mThread)
        mThread.daemon = True
        mThread.start()
        
        dThread = threading.Thread(name="dThread", target=devices_microservice)
        threads.append(dThread)
        dThread.daemon = True
        dThread.start()
    except:
        print("Error in threads creation")

    while(True):
        time.sleep(0.5)