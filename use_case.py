import RPi.GPIO as GPIO
import time
import datetime
import tm1637
from Class import Traffic as Traffic
# import asyncio
import random
from firebase import firebase
import tensorflow as tf
import numpy as np

south = Traffic("south", [1, 24], [22, 27, 17])
west = Traffic("west", [7, 23], [26, 19, 13])
east = Traffic("east", [8, 18], [21, 20, 16])
north = Traffic("north", [25, 15], [6, 5, 0])
tm_south = tm1637.TM1637(clk=south.getSevenSegment()[1], dio=south.getSevenSegment()[0])
tm_west = tm1637.TM1637(clk=west.getSevenSegment()[1], dio=west.getSevenSegment()[0])
tm_east = tm1637.TM1637(clk=east.getSevenSegment()[1], dio=east.getSevenSegment()[0])
tm_north = tm1637.TM1637(clk=north.getSevenSegment()[1], dio=north.getSevenSegment()[0])
tm_south.write([0, 0, 0, 0])
tm_west.write([0, 0, 0, 0])
tm_east.write([0, 0, 0, 0])
tm_north.write([0, 0, 0, 0])
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
red = "red"
green = "green"
yellow = "yellow"
model = tf.keras.models.load_model('ANN')


firebase = firebase.FirebaseApplication('https://dynamic-traffic-light-default-rtdb.firebaseio.com', None)
lst_car =  list(firebase.get('/Vehicle/ruas/', "").values())

def main():
    # init all road
    south = Traffic("south", [1, 24], [22, 27, 17])
    west = Traffic("west", [7, 23], [26, 19, 13])
    east = Traffic("east", [8, 18], [21, 20, 16])
    north = Traffic("north", [25, 15], [6, 5, 0])
    tm_east = tm1637.TM1637(clk=east.getSevenSegment()[1], dio=east.getSevenSegment()[0])
    tm_south = tm1637.TM1637(clk=south.getSevenSegment()[1], dio=south.getSevenSegment()[0])
    tm_west = tm1637.TM1637(clk=west.getSevenSegment()[1], dio=west.getSevenSegment()[0])
    tm_north = tm1637.TM1637(clk=north.getSevenSegment()[1], dio=north.getSevenSegment()[0])
    tm_east.write([0, 0, 0, 0])
    tm_south.write([0, 0, 0, 0])
    tm_west.write([0, 0, 0, 0])
    tm_north.write([0, 0, 0, 0])
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    red = "red"
    green = "green"
    yellow = "yellow"

    road = [south, west, east, north]

    seven_segments = [tm_south, tm_west, tm_east, tm_north]

    # request dari Firebase API
    lst_carr = [4, 6, 7, 9]

    def traffic_cycle(traffic):
        for r in road:
            if r.getArah() == traffic:
                r.light_on(green)
            else:
                r.light_on(red)

    def get_next_road(current_traffic):
        for i, e in enumerate(road):
            if e.getArah() == current_traffic:
                if i == 3:
                    return road[0]
                else:
                    return road[i+1]

    def get_next_tm(tm):
        for i, e in enumerate(seven_segments):
            if e == tm:
                if i == 3:
                    return seven_segments[0]
                else:
                    return seven_segments[i+1]

    for traffic, tm in zip(road, seven_segments):
        # output_green = RNNGenetic.predict(irebaseAPI
       #brtfore
    #nerima aray dari FIrebase API
        # print(model.summary())
        # print(model.predict(np.TM1637Decimalarray([lst_car[0],lst_car[1],lst_car[2],lst_car[3]])[np.newaxis,...]))
        if traffic.getArah()=='south':
            output_green = model.predict(np.array([lst_car[0],lst_car[1],lst_car[2],lst_car[3]])[np.newaxis])
        elif traffic.getArah()=='west':
            output_green = model.predict(np.array([lst_car[1],lst_car[2],lst_car[3],lst_car[0]])[np.newaxis])
        elif traffic.getArah()=='east':
            output_green = model.predict(np.array([lst_car[2],lst_car[3],lst_car[0],lst_car[1]])[np.newaxis])
        elif traffic.getArah()=='north':
            output_green = model.predict(np.array([lst_car[3],lst_car[0],lst_car[1],lst_car[2]])[np.newaxis])
        output_green = int(output_green)
        # output_green = 15

        traffic.setGreenTime(output_green)

        #buat seven segment

        #buat set lampu
        traffic_cycle(traffic.getArah())

        #decreasing time
        while True:
            if traffic.getGreenTime() == 5:
                # arah selanjutanya set merah menjadi 10
                next_road = get_next_road(traffic.getArah())
                next_road.setRedTime(10)
                # seven segment arah next
                tm_next = get_next_tm(tm)
                tm_next.numbers(00, next_road.getRedTime())
                tm.numbers(00, traffic.getGreenTime())
                traffic.updateTime("green")
                next_road.updateTime("red")
            elif traffic.getGreenTime() < 5:
                if traffic.getGreenTime() == 3:
                    traffic.light_on(yellow)
                if traffic.getGreenTime() < 0:
                    traffic.light_on(red)
                    tm.write([0, 0, 0, 0])
                else:
                    tm.numbers(00, traffic.getGreenTime())
                    traffic.updateTime("green")

                if next_road.getRedTime() == 3:
                    next_road.light_on(yellow)
                if next_road.getRedTime() < 0:
                    break
                else:
                    tm_next.numbers(00, next_road.getRedTime())
                    next_road.updateTime("red")
            else:
                tm.numbers(00, traffic.getGreenTime())
                traffic.updateTime("green")
            time.sleep(1)
        tm.write([0, 0, 0, 0])


if __name__ == "__main__":
    try:
        while(True):
            for i in range(4):
                # loop = asyncio.get_event_loop()
                # loop.run_until_complete(main())
                main()
            tm_east.write([0, 0, 0, 0])
            tm_south.write([0, 0, 0, 0])
            tm_west.write([0, 0, 0, 0])
            tm_north.write([0, 0, 0, 0])
            GPIO.cleanup()
    except KeyboardInterrupt:
        tm_east.write([0, 0, 0, 0])
        tm_south.write([0, 0, 0, 0])
        tm_west.write([0, 0, 0, 0])
        tm_north.write([0, 0, 0, 0])
        GPIO.cleanup()