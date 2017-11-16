from sensor_adapters import Sensor
# from sensor_libs.VirtualSensor import *
from sensor_libs import VirtualSensor

class VirtualHumiditySensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        sensor = VirtualSensor.VirtualSensor()
        return sensor.read_humidity()
