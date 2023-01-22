import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

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
        
        time.sleep(5)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
