import random


class VirtualSensor:
    TEMP_AV = 20
    HUM_AV = 50
    PRESS_AV = 100
    GPS_LONG = random.randint(0,600)
    GPS_LAT = random.randint(0,600)

#returns value between 20-30
    @classmethod
    def read_temperature(self):
        temp = self.TEMP_AV
        increase = random.randint(0,10)
        return temp + increase

#returns value between 50-65
    def read_humidity(self):
        hum = self.HUM_AV
        increase = random.randint(0,15)
        return hum + increase

#returns value between 100-130
    def read_pressure(self):
        press = self.PRESS_AV
        increase = random.randint(0,30)
        return press + increase

    #returns
    def read_gps(self):
        VirtualSensor.GPS_LONG += random.randint(-5, 5)
        VirtualSensor.GPS_LAT += random.randint(-5, 5)
        return (self.GPS_LONG, self.GPS_LAT)