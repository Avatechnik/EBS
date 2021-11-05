import RPi.GPIO as GPIO
import time
import datetime
import psutil
from influxdb import InfluxDBClient
import board
import adafruit_dht
# influx configuration - edit these
ifuser = "admin"
ifpass = "admin1"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "system"
# take a timestamp for this measurement
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)


GPIO.setup(2, GPIO.OUT) #LED
GPIO.setup(17, GPIO.IN) #Taster
GPIO.setup(12, GPIO.OUT) #Servo
GPIO.setup(27, GPIO.OUT) #Piezo


p = GPIO.PWM(12, 50) # GPIO 17 als PWM mit 50Hz
p_start=2.5
# for i in range(5):
#     GPIO.output(2, GPIO.HIGH)
#     time.sleep(0.5)
#     GPIO.output(2, GPIO.LOW)
#     time.sleep(0.5)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        #temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
#         print(
#             "Temp: {:.1f} C    Humidity: {}% ".format(
#                  temperature_c, humidity
#             )
       # )
 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        #print(error.args[0])
        #time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        
    
    if GPIO.input(17) == 1:
        GPIO.output(2, GPIO.LOW)
        p.stop()
        GPIO.output(27, GPIO.LOW)
        body = [
    {
        "measurement": measurement_name,
        "time": datetime.datetime.utcnow(),
        "fields": {
            "temperatur": temperature_c,
            "humidity": humidity,
            "taster": 0,
            "piezo": 0,
            "LED": 0,
            "Servo": 2.5 
        }
    }
]
        ifclient.write_points(body)
    else:
        body = [
    {
        "measurement": measurement_name,
        "time": datetime.datetime.utcnow(),
        "fields": {
            "temperatur": temperature_c,
            "humidity": humidity,
            "taster": 1,
            "piezo": 1,
            "LED": 1,
            "Servo": 2.5 
        }
    }
]
        ifclient.write_points(body)
        GPIO.output(2, GPIO.HIGH)
        body = [
    {
        "measurement": measurement_name,
        "time": datetime.datetime.utcnow(),
        "fields": {
            "temperatur": temperature_c,
            "humidity": humidity,
            "taster": 1,
            "piezo": 1,
            "LED": 1,
            "Servo": 2.5 
        }
    }
]
        ifclient.write_points(body)
        p.start(p_start)
        axel = p_start
        
        p.ChangeDutyCycle(axel)
        axel+= p_start
        body = [
    {
        "measurement": measurement_name,
        "time": datetime.datetime.utcnow(),
        "fields": {
            "temperatur": temperature_c,
            "humidity": humidity,
            "taster": 1,
            "piezo": 1,
            "LED": 1,
            "Servo": axel 
        }
    }
]
        ifclient.write_points(body)
        GPIO.output(27, GPIO.HIGH)
        #time.sleep(0.5)
        GPIO.output(27, GPIO.LOW)
        #time.sleep(0.5)
