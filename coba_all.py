import RPi.GPIO as GPIO
import tm1637
import time

GPIO.setmode(GPIO.BCM)

#lampu 1 - Selatan
red = 22
yellow = 27
green = 17

GPIO.setup(red,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)

#lampu 2 - Barat
red_2 = 26
yellow_2 = 19
green_2= 13

GPIO.setup(red_2,GPIO.OUT)
GPIO.setup(yellow_2,GPIO.OUT)
GPIO.setup(green_2,GPIO.OUT)

#lampu 3 - Utara
red_3 = 6
yellow_3 = 5
green_3 = 0

GPIO.setup(red_3,GPIO.OUT)
GPIO.setup(yellow_3,GPIO.OUT)
GPIO.setup(green_3,GPIO.OUT)

#lampu 4 - Timur
red_4 = 21
yellow_4 = 20
green_4 = 16

GPIO.setup(red_4,GPIO.OUT)
GPIO.setup(yellow_4,GPIO.OUT)
GPIO.setup(green_4,GPIO.OUT)

# tm 1 - barat
tm_barat = tm1637.TM1637(clk=23, dio=7)

# tm 2 - selatan
tm_selatan = tm1637.TM1637(clk=24, dio=1)

# tm 3 - utara
tm_utara = tm1637.TM1637(clk=15, dio=25)

# # tm 4 - timur
tm_timur = tm1637.TM1637(clk=18, dio=8)


try:
    while True:
        tm_selatan.numbers(1, 30)
        tm_barat.numbers(2, 21)
        tm_timur.numbers(3, 26)
        tm_utara.numbers(4, 45)

        # GPIO.output(red,True)
        # GPIO.output(yellow,False)
        # GPIO.output(green,False)

        # GPIO.output(red_2,True)
        # GPIO.output(yellow_2,False)
        # GPIO.output(green_2,False)

        # GPIO.output(red_3,True)
        # GPIO.output(yellow_3,False)
        # GPIO.output(green_3,False)

        GPIO.output(red_4,True)
        GPIO.output(yellow_4,False)
        GPIO.output(green_4,False)

        time.sleep(1)

        # GPIO.output(red,False)
        # GPIO.output(yellow,True)
        # GPIO.output(green,False)

        # GPIO.output(red_2,False)
        # GPIO.output(yellow_2,True)
        # GPIO.output(green_2,False)

        # GPIO.output(red_3,False)
        # GPIO.output(yellow_3,True)
        # GPIO.output(green_3,False)

        GPIO.output(red_4,False)
        GPIO.output(yellow_4,True)
        GPIO.output(green_4,False)

        time.sleep(1)

        # GPIO.output(red,False)
        # GPIO.output(yellow,False)
        # GPIO.output(green,True)

        # GPIO.output(red_2,False)
        # GPIO.output(yellow_2,False)
        # GPIO.output(green_2,True)

        # GPIO.output(red_3,False)
        # GPIO.output(yellow_3,False)
        # GPIO.output(green_3,True)

        GPIO.output(red_4,False)
        GPIO.output(yellow_4,False)
        GPIO.output(green_4,True)
        
        time.sleep(1)

except KeyboardInterrupt:
    tm_barat.write([0, 0, 0, 0])
    tm_selatan.write([0, 0, 0, 0])
    tm_utara.write([0, 0, 0, 0])
    tm_timur.write([0, 0, 0, 0])
    GPIO.cleanup()

