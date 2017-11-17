
from sensor_adapters import VirtualTemperatureSensor, VirtualPressureSensor, VirtualHumiditySensor, VirtualGpsSensor

class SensorDataProvidersFactoryTest:

    @staticmethod
    def get_data_provider(name, type, connection=None):
        # VIRTUAL SENSOR data retrivial
        if name == 'virtual':
            if type == 'temperature':
                sensor = VirtualTemperatureSensor.VirtualTemperatureSensor(name, name, type)
                return sensor
            if type == 'humidity':
                sensor = VirtualHumiditySensor.VirtualHumiditySensor(name, name, type)
                return sensor
            if type == 'pressure':
                sensor = VirtualPressureSensor.VirtualPressureSensor(name, name, type)
                return sensor
            if type == 'gps':
                sensor = VirtualGpsSensor.VirtualGpsSensor(name, name, type)
                return sensor
            else:
                pass

