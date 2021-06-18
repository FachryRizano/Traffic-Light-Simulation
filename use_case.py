import RPi.GPIO as GPIO
import time
import datetime
import tm1637
from Class import Traffic as Traffic
# import asyncio
import random
import tensorflow as tf

selatan = Traffic("selatan", [1, 24], [22, 27, 17])
barat = Traffic("barat", [7, 23], [26, 19, 13])
timur = Traffic("timur", [8, 18], [6, 5, 0])
utara = Traffic("utara", [25, 15], [21, 20, 16])
tm_timur = tm1637.TM1637(clk=timur.getSevenSegment()[1], dio=timur.getSevenSegment()[0])
tm_selatan = tm1637.TM1637(clk=selatan.getSevenSegment()[1], dio=selatan.getSevenSegment()[0])
tm_barat = tm1637.TM1637(clk=barat.getSevenSegment()[1], dio=barat.getSevenSegment()[0])
tm_utara = tm1637.TM1637(clk=utara.getSevenSegment()[1], dio=utara.getSevenSegment()[0])
tm_timur.write([0, 0, 0, 0])
tm_selatan.write([0, 0, 0, 0])
tm_barat.write([0, 0, 0, 0])
tm_utara.write([0, 0, 0, 0])
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
red = "red"
green = "green"
yellow = "yellow"
model = tf.keras.models.load_model('ANN/saved_model.pb')

def main():
    # init semua ruas
    selatan = Traffic("selatan", [1, 24], [22, 27, 17])
    barat = Traffic("barat", [7, 23], [26, 19, 13])
    timur = Traffic("timur", [8, 18], [6, 5, 0])
    utara = Traffic("utara", [25, 15], [21, 20, 16])
    tm_timur = tm1637.TM1637(clk=timur.getSevenSegment()[1], dio=timur.getSevenSegment()[0])
    tm_selatan = tm1637.TM1637(clk=selatan.getSevenSegment()[1], dio=selatan.getSevenSegment()[0])
    tm_barat = tm1637.TM1637(clk=barat.getSevenSegment()[1], dio=barat.getSevenSegment()[0])
    tm_utara = tm1637.TM1637(clk=utara.getSevenSegment()[1], dio=utara.getSevenSegment()[0])
    tm_timur.write([0, 0, 0, 0])
    tm_selatan.write([0, 0, 0, 0])
    tm_barat.write([0, 0, 0, 0])
    tm_utara.write([0, 0, 0, 0])
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    red = "red"
    green = "green"
    yellow = "yellow"

    ruas = [selatan, barat, timur, utara]

    seven_segments = [tm_selatan, tm_barat, tm_timur, tm_utara]

    # request dari Firebase API
    lst_carr = [4, 6, 7, 9]

    def rotasi_lampu(traffic):
        for r in ruas:
            if r.getArah() == traffic:
                r.light_on(green)
            else:
                r.light_on(red)

    def get_arah_selanjutnya(traffic_sekarang):
        for i, e in enumerate(ruas):
            if e.getArah() == traffic_sekarang:
                if i == 3:
                    return ruas[0]
                else:
                    return ruas[i+1]

    def tm_selanjutnya(tm):
        for i, e in enumerate(seven_segments):
            if e == tm:
                if i == 3:
                    return seven_segments[0]
                else:
                    return seven_segments[i+1]

    for traffic, tm in zip(ruas, seven_segments):
        # output_green = RNNGenetic.predict(FirebaseAPI)
        #brutefore
        #nerima array dari FIrebase API
        if traffic.getArah()=='selatan':
            output_green = model.predict(arr[0],arr[1],arr[2],arr[3])
        elif traffic.getArah()=='barat':
            output_green = model.predict(arr[1],arr[2],arr[3],arr[0])
        elif traffic.getArah()=='timur':
            output_green = model.predict(arr[2],arr[3],arr[0],arr[1])
        else:
            output_green = model.predict(arr[3],arr[0],arr[1],arr[2])
        # output_green = random.randint(10, 15)
        traffic.setGreenTime(output_green)

        #buat seven segment

        #buat set lampu
        rotasi_lampu(traffic.getArah())

        #decreasing time
        while True:
            if traffic.getGreenTime() == 5:
                # arah selanjutanya set merah menjadi 10
                arah_next = get_arah_selanjutnya(traffic.getArah())
                arah_next.setRedTime(10)
                # seven segment arah next
                tm_next = tm_selanjutnya(tm)
                tm_next.numbers(00, arah_next.getRedTime())
                tm.numbers(00, traffic.getGreenTime())
                traffic.updateTime("green")
                arah_next.updateTime("red")
            elif traffic.getGreenTime() < 5:
                if traffic.getGreenTime() == 3:
                    traffic.light_on(yellow)
                if traffic.getGreenTime() < 0:
                    traffic.light_on(red)
                    tm.write([0, 0, 0, 0])
                else:
                    tm.numbers(00, traffic.getGreenTime())
                    traffic.updateTime("green")

                tm_next.numbers(00, arah_next.getRedTime())
                arah_next.updateTime("red")
                if arah_next.getRedTime() == 2:
                    arah_next.light_on(yellow)
                if arah_next.getRedTime() < -1:
                    break

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
                tm_timur.write([0, 0, 0, 0])
                tm_selatan.write([0, 0, 0, 0])
                tm_barat.write([0, 0, 0, 0])
                tm_utara.write([0, 0, 0, 0])
                GPIO.cleanup()
    except KeyboardInterrupt:
        tm_timur.write([0, 0, 0, 0])
        tm_selatan.write([0, 0, 0, 0])
        tm_barat.write([0, 0, 0, 0])
        tm_utara.write([0, 0, 0, 0])
        GPIO.cleanup()