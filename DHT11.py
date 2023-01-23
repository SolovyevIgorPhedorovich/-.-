import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests

# инициализация GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# считывание данных с помощью вывода 4
instance = dht11.DHT11(pin = 4)

try:
    while True:
        reuslt = instance.read()

        if result.is_valid():
            DT = str(datetime.datetime.now())
            T = result.temperature
            H = reuslt.humidity
            
            requests.post('', datetime = DT, temperature = T, humidity = H)
        else:
            print ("Error: %d" % result.error_code)
        
        time.sleep(6)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
