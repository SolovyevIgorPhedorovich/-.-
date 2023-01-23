import RPi.GPIO as GPIO
import lirc
import DHT11
import post

# инициализация GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

#conditioner_status
try:
    #Включаем кондионер
    if conditioner_status == True and post.conditioner_status == False:
        client = lirc.Client("name_1","18")
        conditioner_status = post.conditioner_status
    
    #Уменьшаем температуру
    if DHT11.T > post.optional_temperature:
        if conditioner_status == True:
            client = lirc.Client("temp_1","15")
        else:                                                   #Если кондиционер выключен
            conditioner_status = True
            client = lirc.Client("name_0","17")
            client = lirc.Client("temp_2","16")

    #Увеличиваем температуру
    if DHT11.T < post.optional_temperature:
        if conditioner_status == True:
            client = lirc.Client("temp_1","15")
        else:
            conditioner_status = True                            #Если кондиционер выключен
            client = lirc.Client("name_0","17")
            client = lirc.Client("temp_2","16")

    #Выключаем кондионер
    if DHT11.T == post.optional_temperature or DHT11.T == post.optional_temperature - 2 or DHT11.T == post.optional_temperature + 2:
        client = lirc.Client("name_0","17")
        conditioner_status = False

    

except lirc.exceptions.LircdCommandFailureError as error:
    f = open("error_log.txt", "w")
    f.write("Unable to send the power key!: " + error)
    f.close
