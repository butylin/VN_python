from sensor_adapters import Sensor
from sensor_libs.VirtualSensor import *

class VirtualHumiditySensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        sensor = VirtualSensor()
        return sensor.read_humidity()
