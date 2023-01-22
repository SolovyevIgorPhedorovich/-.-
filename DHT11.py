import RPi.GPIO as GPIO
import dht11
import time
import datetime

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

instance = dht11.DHT11(pin = 4)

try:
    while True:
        reuslt = instance.read()

        if result.is_valid():
            print ("Last valid input: " + str(datetime.datetime.now()))
            print ("Temperature: %-3.1f C" % result.temperature)
            print ("Humidity: %-3.1f %%" % reuslt.humidity)
        else:
            print ("Error: %d" % result.error_code)
        
        time.sleep(5)

except :
    print("Cleanup")
    GPIO.cleanup()
