from sensors import VirtualTemperatureSensor, VirtualPressureSensor, VirtualHumiditySensor, VirtualGpsSensor, Adafruit_BME280_temperature


class SensorDataProvidersFactory:

    @staticmethod
    def get_data_provider(name, type):
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
                return "Unknown sensor!"
        if name == 'Adafruit_BME280':
            if type == 'temperature':
                sensor = Adafruit_BME280_temperature.Adafruit_BME280_temperature(name, name, type)
                return sensor
            if type == 'humidity':
                sensor = Adafruit_BME280_temperature.Adafruit_BME280_temperature(name, name, type)
                return sensor
            if type == 'pressure':
                sensor = Adafruit_BME280_temperature.Adafruit_BME280_temperature(name, name, type)
                return sensor
            else:
                return "Unknown sensor!"
