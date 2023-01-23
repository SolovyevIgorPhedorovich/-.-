import RPi.GPIO as GPIO
import dht11
import time
import datetime

# инициализация GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# считывание данных с помощью вывода 4
instance = dht11.DHT11(pin = 4)

reuslt = instance.read()

if result.is_valid():
    DT = str(datetime.datetime.now())
    T = result.temperature
    H = reuslt.humidity
else:
    F = open('example.txt','w')
    F.write("Error: %d" % result.error_code)
    F.close() 

GPIO.cleanup()
