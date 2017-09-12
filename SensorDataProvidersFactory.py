from sensors import VirtualTemperatureSensor, VirtualPressureSensor, VirtualHumiditySensor, VirtualGpsSensor, \
                    Adafruit_BME280_temperature, Adafruit_BME280_humidity, Adafruit_BME280_pressure, \
                    Adafruit_TCS34725_RGB, LED_light


class SensorDataProvidersFactory:

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
        if name == 'Adafruit_BME280':
            if type == 'temperature':
                sensor = Adafruit_BME280_temperature.Adafruit_BME280_temperature(name, name, type)
                return sensor
            if type == 'humidity':
                sensor = Adafruit_BME280_humidity.Adafruit_BME280_humidity(name, name, type)
                return sensor
            if type == 'pressure':
                sensor = Adafruit_BME280_pressure.Adafruit_BME280_pressure(name, name, type)
                return sensor
            else:
                return "Unknown sensor!"
        if name == 'Adafruit_TCS34725':
            if type == 'light':
                sensor = Adafruit_TCS34725_RGB.Adafruit_TCS34725_RGB(name, name, type)
                return sensor
            else:
                pass
        # OUTPUTS
        if name == 'led':
            output = LED_light.LED_light(name, name, type, connection)
            return output
        else:
            pass

