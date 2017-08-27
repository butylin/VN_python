from sensors import Sensor
from Adafruit_BME280 import *

class Adafruit_BME280_humidity(Sensor.Sensor):

    @classmethod
    def get_data(self):
        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
        degrees = sensor.read_humidity()
        return degrees

        # pascals = sensor.read_pressure()
        # hectopascals = pascals / 100
        # humidity = sensor.read_humidity()
        #
        # print 'Temp      = {0:0.3f} deg C'.format(degrees)
        # print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        # print 'Humidity  = {0:0.2f} %'.format(humidity)

