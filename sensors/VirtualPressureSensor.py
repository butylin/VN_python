from sensors import Sensor
from VirtualSensor import *

class VirtualPressureSensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        sensor = VirtualSensor()
        return sensor.read_pressure()
