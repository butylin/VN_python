from sensor_adapters import Sensor
# from sensor_libs.VirtualSensor import *
from sensor_libs import VirtualSensor

class VirtualTemperatureSensor(Sensor.Sensor):

    @classmethod
    def get_data(self):
        temp_sensor = VirtualSensor.VirtualSensor()
        return temp_sensor.read_temperature()

