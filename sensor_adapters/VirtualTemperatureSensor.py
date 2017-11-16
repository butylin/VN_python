from sensor_adapters import Sensor
from sensor_libs.VirtualSensor import *


class VirtualTemperatureSensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        temp_sensor = VirtualSensor()
        return temp_sensor.read_temperature()

