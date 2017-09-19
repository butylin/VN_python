import time, datetime

from SensorDataProvidersFactory import *
from DBDevicesProvider import DevicesData
from DBSensorReadingsProvider import SensorReadingsData
from MQTTHandshakeHandler import MQTTHandshakeHandler

# sensorData = SensorReadingsData()
#
# sensorData.add_sensor_reading(datetime.datetime.now(), 'test', '123')
# sensorData.add_sensor_reading(datetime.datetime.now(), 'test', '567')

class Main():
    def __init__(self, db_sensor_readings=None):
        self.db_sensor_readings = db_sensor_readings
        self.mode_online = False

    def start(self):
        devices_data = DevicesData()
        sensors_data = SensorReadingsData()
        # sensors_data = self.db_sensor_readings()
        hadshake_handler = MQTTHandshakeHandler()

        sensors = []
        outputs = {}
        leds = {}

        # getting list of records for sensors and output devices from DB
        sensor_data_list = devices_data.get_all_sensors()
        output_list = devices_data.get_all_outputs()

        # making a list of output device providers to work with
        for output in output_list:
            print('Output name: {} Type: {} Connection: {}'.format(output.name, output.type, output.connection))
            if output.name == 'led':
                out_provider = SensorDataProvidersFactory.get_data_provider(output.name, output.type, output.connection)
                leds[output.type] = out_provider
                outputs['leds'] = leds
                print("Sensor provider: ", out_provider)
            else:
                out_provider = SensorDataProvidersFactory.get_data_provider(output.name, output.type, output.connection)
                outputs[output.name] = out_provider

        print(outputs)

        # making a list of sensor provides providers to work with
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

        # attempting to do a handshake with Roaming Node to retrieve the SLN-node
        SLN_current = hadshake_handler.do_handshake()

        # if handshake returns best SLN, go to ONLINE mode
        if SLN_current == 0 or SLN_current == 1 or SLN_current == 2:
            print("Working in OFFLINE-mode")
            # if Blue LED is initialised, turn it on
            if leds['blue'] is not None:
                leds['blue'].on()
        else:
            self.mode_online = True
            print("Working in ONLINE-mode")
            # if Green LED is initialised, turn it on
            if leds['green'] is not None:
                leds['green'].on()


        while True:
            leds['red'].on()
            for sensor in sensors:
                print("{}({}): {}".format(sensor.name, sensor.type, sensor.get_data()))
            print('******************')
            leds['red'].off()
            time.sleep(1)

    def add_to_db(self):
        devices_data = DevicesData()

        devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280 Temperature Sensor', 'temperature', 'GPIO2, GPIO3, I2C: 0x77')
        devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280 Humidity Sensor', 'humidity', 'GPIO2, GPIO3, I2C: 0x77')
        devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280l Pressure Sensor', 'pressure', 'GPIO2, GPIO3, I2C: 0x77')
        devices_data.add_sensor('Adafruit_TCS34725', 'Adafruit_TCS34725 Light Sensor', 'light', 'I2C 0x29', False)

        devices_data.add_output('led', 'LED Green', 'green', '26')
        devices_data.add_output('led', 'LED Red', 'red', '13')
        devices_data.add_output('console', 'Console Output', 'console', '')

        # devices_datacalc.add_sensor('virtual', 'Virtual Temperature Sensor', 'temperature', 'virtual')
        # devices_data.add_sensor('humid_virt', 'Virtual Humidity Sensor', 'humidity', 'virtual')
        # devices_data.add_sensor('gps_virt', 'Virtual GPS Sensor', 'gps', 'virtual')

        devices_data.close()

        connected_to_SLN = False
        SLN_current = None


# main = Main(SensorReadingsData())
main = Main()
main.start()




