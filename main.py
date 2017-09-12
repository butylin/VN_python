import time, datetime

from SensorDataProvidersFactory import *
from DBDevicesProvider import DevicesData
from DBSensorReadingsProvider import SensorReadingsData

# sensorData = SensorReadingsData()
#
# sensorData.add_sensor_reading(datetime.datetime.now(), 'test', '123')
# sensorData.add_sensor_reading(datetime.datetime.now(), 'test', '567')

def add_to_db():
    devices_data = DevicesData()

    devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280 Temperature Sensor', 'temperature', 'GPIO2, GPIO3, I2C: 0x77')
    devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280 Humidity Sensor', 'humidity', 'GPIO2, GPIO3, I2C: 0x77')
    devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280l Pressure Sensor', 'pressure', 'GPIO2, GPIO3, I2C: 0x77')
    devices_data.add_sensor('Adafruit_TCS34725', 'Adafruit_TCS34725 Light Sensor', 'light', 'I2C 0x29', False)

    devices_data.add_output('led', 'LED Green', 'green', '26')
    devices_data.add_output('led', 'LED Red', 'red', '13')
    devices_data.add_output('console', 'Console Output', 'console', '')

    # devices_data.add_sensor('virtual', 'Virtual Temperature Sensor', 'temperature', 'virtual')
    # devices_data.add_sensor('humid_virt', 'Virtual Humidity Sensor', 'humidity', 'virtual')
    # devices_data.add_sensor('gps_virt', 'Virtual GPS Sensor', 'gps', 'virtual')

    devices_data.close()

def main():

    devices_data = DevicesData()
    sensors_data = SensorReadingsData()

    sensors = []
    sensor_data_list = devices_data.get_all_sensors()

    for sensor_data in sensor_data_list:
        print('Sensor name: {}\nSensor type: {}\nConnection: {}\nActive: {}'.format(sensor_data.name, sensor_data.type, sensor_data.connection, sensor_data.active))
        if sensor_data.active:
            sensor_provider = SensorDataProvidersFactory.get_data_provider(sensor_data.name, sensor_data.type)
            if sensor_provider != None:
                sensors.append(sensor_provider)
            print("Sensor provider: ", sensor_provider)

        else:
            print("Sensor DEACTIVATED!")
        print('********************************')

    while True:
            for sensor in sensors:
                print("{}({}): {}".format(sensor.name, sensor.type, sensor.get_data()))
            print('******************')
            time.sleep(1);


# add_to_db()
main()




