from sensor_adapters import Sensor
from sensor_libs.VirtualSensor import *

class VirtualGpsSensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        temp_sensor = VirtualSensor()
        return temp_sensor.read_gps()
