import RPi.GPIO as GPIO
#import asyncio
class Traffic:

    def __init__(self,arah,seven_segment,pinTraffic):
        self.__arah = arah
        self.__seven_segment = seven_segment
        self.__pinTraffic = pinTraffic
    
    def getArah(self):
        return self.__arah
        
    def getSevenSegment(self):
        return self.__seven_segment

    def getGreenTime(self):
        return self.__greentime
    
    def getRedTime(self):
        return self.__redtime

    def getStatus(self):
        return self.__status
    
    def countGreenTime(self,total_kendaraan):
        threshold = 15
        waktu = total_kendaraan*2
        if waktu >= threshold:
            return threshold
        else:
            return waktu

    def updateTime(self,time):
        if time == "green":
            self.__greentime -= 1
        elif time == "red":
            self.__redtime -= 1
    
    def setStatus(self,status):
        self.__status = status

    def setGreenTime(self,greenTime):
        self.__greentime = greenTime

    def setRedTime(self,time):
        self.__redtime = time

    def countRedTime(self,prev):
        return prev.getGreenTime() + prev.getRedTime() + 3

    def getPinTraffic(self):
        return self.__pinTraffic

    def light_on(self,color):
        for i in range(3):
            GPIO.setup(self.getPinTraffic()[i],GPIO.OUT)
        
        if color == "red":
            GPIO.output(self.getPinTraffic()[0],True)
            GPIO.output(self.getPinTraffic()[1],False)
            GPIO.output(self.getPinTraffic()[2],False)
        elif color == "green":
            GPIO.output(self.getPinTraffic()[0],False)
            GPIO.output(self.getPinTraffic()[1],False)
            GPIO.output(self.getPinTraffic()[2],True)
        elif color == "yellow":
            GPIO.output(self.getPinTraffic()[0],False)
            GPIO.output(self.getPinTraffic()[1],True)
            GPIO.output(self.getPinTraffic()[2],False)