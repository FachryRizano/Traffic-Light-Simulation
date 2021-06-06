import RPi.GPIO as GPIO
import time
import datetime
import tm1637
from Class import Traffic as Traffic
# import asyncio


#init semua ruas
selatan = Traffic("selatan",[1, 24],[22,27,17]) 
barat = Traffic("barat",[7, 23],[26,19,13])
timur = Traffic("timur",[8, 18],[6,5,0])
utara = Traffic("utara",[25, 15],[21,20,16])
tm_timur= tm1637.TM1637(clk=timur.getSevenSegment()[1],dio=timur.getSevenSegment()[0])
tm_selatan = tm1637.TM1637(clk=selatan.getSevenSegment()[1],dio=selatan.getSevenSegment()[0])
tm_barat = tm1637.TM1637(clk=barat.getSevenSegment()[1],dio=barat.getSevenSegment()[0])
tm_utara = tm1637.TM1637(clk=utara.getSevenSegment()[1],dio=utara.getSevenSegment()[0])

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


ruas = {'selatan':selatan,
    'barat':barat,
    'timur':timur,
'utara':utara}

seven_segments = [tm_selatan,tm_barat,tm_timur,tm_utara]
green = "green"
red = "red"
yellow = "yellow"

#request dari Firebase API
lst_carr=[4,6,7,9]
def rotasi_lampu(traffic):
    for r in ruas.keys():
        if r==traffic:
            ruas[r].light_on(green)
        else:
            ruas[r].light_on(red)  

def get_arah_selanjutnya(traffic_sekarang):
    for i,k in enumerate(ruas.keys()):
        if k==traffic_sekarang:
            return ruas.values()[i] 
try:
    while(True):
        GPIO.cleanup()
        for traffic,tm in zip(ruas.values(),seven_segments):
            output_green = 10
            traffic.setGreenTime(output_green)

            #buat seven segment
            tm.numbers(00,traffic.getGreenTime())

            #buat set lampu
            rotasi_lampu(traffic.getArah())
            
            #decreasing time
            for i in range(traffic.getGreenTime()):
                traffic.updateTime("green")
                time.sleep(1)
                # if traffic.getGreenTime()==5:
                #     #arah selanjutanya set merah menjadi 10
                #     arah_next = get_arah_selanjutnya(traffic.getArah())
                #     arah_next.setRedTime(10)
                #     #seven segment arah next
                #     i = [i for i,e in enumerate(ruas.values()) if e==arah_next]
                #     tm_next = seven_segments[i]

        
except KeyboardInterrupt:
    tm_timur.write([0, 0, 0, 0])
    tm_selatan.write([0,0,0,0])
    tm_barat.write([0,0,0,0])
    tm_utara.write([0,0,0,0])
    GPIO.cleanup()
# tm_.numbers()
# timur.updateTime(green)
# async def timurCountdown():
#     while timur.getGreenTime() > -1:
#         tm_timur.numbers(00,timur.getGreenTime())
#         tm_selatan.numbers(00,selatan.getRedTime())
#         tm_barat.numbers(00,barat.getRedTime())
#         tm_utara.numbers(00,utara.getRedTime())
#         await asyncio.sleep(1)
#         timur.updateTime(green)
#         selatan.updateTime(red)
#         barat.updateTime(red)
#         utara.updateTime(red)
#         if timur.getGreenTime() == 0:
#             break


# async def selatanCountdown():
#     while selatan.getGreenTime() > -1:
#         tm_timur.numbers(00,timur.getRedTime())
#         tm_selatan.numbers(00,selatan.getGreenTime())
#         tm_barat.numbers(00,barat.getRedTime())
#         tm_utara.numbers(00,utara.getRedTime())
#         await asyncio.sleep(1)
#         timur.updateTime(red)
#         selatan.updateTime(green)
#         barat.updateTime(red)
#         utara.updateTime(red)    
    
# async def baratCountdown():
#     while barat.getGreenTime() > -1:
#         tm_timur.numbers(00,timur.getRedTime())
#         tm_selatan.numbers(00,selatan.getRedTime())
#         tm_barat.numbers(00,barat.getGreenTime())
#         tm_utara.numbers(00,utara.getRedTime())
#         await asyncio.sleep(1)
#         timur.updateTime(red)
#         selatan.updateTime(red)
#         barat.updateTime(green)
#         utara.updateTime(red)
#     utaraCountdown()

# async def utaraCountdown():
#     while utara.getGreenTime() > -1:
#         tm_timur.numbers(00,timur.getRedTime())
#         tm_selatan.numbers(00,selatan.getRedTime())
#         tm_barat.numbers(00,barat.getRedTime())
#         tm_utara.numbers(00,utara.getGreenTime())
#         await asyncio.sleep(1)
#         timur.updateTime(red)
#         selatan.updateTime(red)
#         barat.updateTime(red)
#         utara.updateTime(green)

# async def transisiLampu():
#     timur.light_on(yellow)
#     await asyncio.sleep(1)
    
#     timur.light_on(red)
#     await asyncio.sleep(1)
#     selatan.light_on(yellow)
#     await asyncio.sleep(1)
#     selatan.light_on(green)
#     await asyncio.sleep(selatan.getGreenTime())

#Fungsi transisi lampu
# async def lampTransition(object):
#     if obj.getGreenTime() == 0:
#         obj.light_on(yellow)
#         await asyncio.sleep(1)
#         obj.light_on(red)
#     else obj.getRedTime()==0:
#         obj.light_on(yellow)
#         await asyncio.sleep(1)
#         obj.light_on(green)

#Fungsi transisi waktu
# async def timeTransition():
    #set waktu ketika lampu merah nyala
    #set waktu ketika lampu hijau nyala

#Fungsi transisi lampu 
#greentime decreasing sampe 0
#1 detik (untuk yellow light)
#ganti waktu red time decreasing

# def main():
#     timur.light_on(green)
#     selatan.light_on(red)
#     barat.light_on(red)
#     utara.light_on(red)
#     asyncio.gather(timurCountdown())
#     await asyncio.sleep(timur.getGreenTime())
#     asyncio.gather(transisiLampu())
#     asyncio.gather(selatanCountdown())
#     await asyncio.sleep(selatan.getGreenTime())
    
    # await asyncio.sleep(3)
    # loop.stop()

# if __name__ == "__main__":
#     try:    
#         while(True):
#             loop = asyncio.get_event_loop()
#             loop.run_until_complete(main())
#     except KeyboardInterrupt:
#         tm_timur.write([0, 0, 0, 0])
#         tm_selatan.write([0,0,0,0])
#         tm_barat.write([0,0,0,0])
#         tm_utara.write([0,0,0,0])    
#         GPIO.cleanup()
    
#     finally:
#         loop.close()
