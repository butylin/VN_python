from sensors import Sensor
from VirtualSensor import *

class VirtualHumiditySensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        sensor = VirtualSensor()
        return sensor.read_humidity()
