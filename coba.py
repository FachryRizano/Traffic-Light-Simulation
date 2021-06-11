import RPi.GPIO as GPIO
import time
# GPIO.setwarnings(False)
import tm1637
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

red = 22
yellow = 27
green = 17

red_2 = 26
yellow_2 = 19
green_2= 13

GPIO.setup(red,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)

GPIO.setup(red_2,GPIO.OUT)
GPIO.setup(yellow_2,GPIO.OUT)
GPIO.setup(green_2,GPIO.OUT)

tm_barat = tm1637.TM1637(clk=7, dio=23)
counter = 50
try:
    while counter:
        # GPIO.output(green,True)
        # GPIO.output(red,False)
        # GPIO.output(yellow,False)
        # GPIO.output(green_2,True)
        # GPIO.output(red_2,False)
        # GPIO.output(yellow_2,False)
        # time.sleep(1)

        # GPIO.output(green,False)
        # GPIO.output(yellow,True)
        # GPIO.output(red,False)
        # GPIO.output(green_2,False)
        # GPIO.output(yellow_2,True)
        # GPIO.output(red_2,False)
        
        # time.sleep(1)

        # GPIO.output(green,False)
        # GPIO.output(yellow,False)
        # GPIO.output(red,True)
        # GPIO.output(green_2,False)
        # GPIO.output(yellow_2,False)
        # GPIO.output(red_2,True)
        tm_barat.numbers(00,counter)
        time.sleep(1)
        counter -=1
    print("kelar try")
    GPIO.cleanup()
except KeyboardInterrupt:
    print("test")
    GPIO.cleanup()

# GPIO.cleanup()