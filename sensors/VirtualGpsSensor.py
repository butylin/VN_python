from sensors import Sensor
from VirtualSensor import *

class VirtualGpsSensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        temp_sensor = VirtualSensor()
        return temp_sensor.read_gps()
