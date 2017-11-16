import time, datetime
import json

from SensorDataProvidersFactory import *
from DBDevicesProvider import DevicesData
from DBSensorReadingsProvider import SensorReadingsData
from MQTTHandshakeHandler import MQTTHandshakeHandler
from utils.VN_Config import VN_Config
from utils.VN_Logger import VNLogger

config = VN_Config.getInstance().getConfig()
VID = config['SETTINGS']['VIN']
THRESHOLDS = {
    'temperature': 29,
    'pressure': 1000,
    'humidity': 60
              }

# sensorData = SensorReadingsData()
#
# sensorData.add_sensor_reading(datetime.datetime.now(), 'test', '123')
# sensorData.add_sensor_reading(datetime.datetime.now(), 'test', '567')

class Main():
    def __init__(self, db_sensor_readings=None):
        self.db_sensor_readings = db_sensor_readings
        self.mode_online = False
        self.leds = {}
        self.VID = VID
        self.devices_data = DevicesData()
        self.sensors_data = SensorReadingsData()
        self.sensor_readings_db_created = date_stamp = datetime.datetime.now().strftime('%d-%m-%y')

        mylogger = VNLogger.getInstance().getLogger()

        # sensors_data = self.db_sensor_readings()




    def start(self):

        sensors = []
        outputs = {}
        hadshake_handler = MQTTHandshakeHandler()

        # getting list of records for sensors and output devices from DB
        sensor_data_list = self.devices_data.get_all_sensors()
        output_list = self.devices_data.get_all_outputs()
        outputs = self.outputs_init(output_list)
        sensors = self.sensors_init(sensor_data_list)

        # attempting to do a handshake with Roaming Node to retrieve the SLN-node
        SLN_current = hadshake_handler.do_handshake()

        # if handshake returns best SLN, go to ONLINE mode
        # TODO: catch exceptions instead of integer values
        if SLN_current == 0 or SLN_current == 1 or SLN_current == 2:
            self.set_mode_offline(self.leds)
        else:
            self.set_mode_online(self.leds)

        # main loop
        # getting data from sensors
        print("*********************************")
        while True:
            values = {}
            values_cr = {}
            for sensor in sensors:
                key_n = str(sensor.name)
                key_t = str(sensor.type)
                key = (key_n + "::" + key_t)
                value = sensor.get_data()

                if self.is_critical(key_t, value):
                    self.led_on('red')
                    values_cr[key] = value

                values[key] = value
                print("{}({}): {}".format(sensor.name, sensor.type, sensor.get_data()))
            print("*********************************")

            json_str = json.dumps(values)
            self.save_sensor_readings(values)
            time.sleep(1)
            self.led_off('red')
            print("CRIT!: ", values_cr)

    def is_critical(self, key_t, value):
       if THRESHOLDS.__contains__(key_t) and value >= THRESHOLDS[key_t]:
           return True
       else:
           return False


    def sensors_init(self, sensor_data_list):
        # making a list of sensor provides providers to work with
        sensors = []
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

        return sensors

    def outputs_init(self, output_list):
        # making a list of output device providers to work with
        outputs = {}
        for output in output_list:
            print('Output name: {} Type: {} Connection: {}'.format(output.name, output.type, output.connection))
            if output.name == 'led':
                out_provider = SensorDataProvidersFactory.get_data_provider(output.name, output.type, output.connection)
                self.leds[output.type] = out_provider
                outputs['leds'] = self.leds
                print("Sensor provider: ", out_provider)
            else:
                out_provider = SensorDataProvidersFactory.get_data_provider(output.name, output.type, output.connection)
                outputs[output.name] = out_provider

        # print(outputs)
        return outputs

    def set_mode_online(self, leds):
        self.mode_online = True
        self.led_on('green')
        self.led_off('blue')
        print("Working in ON-LINE-mode")

    def set_mode_offline(self, leds):
        self.mode_online = False
        self.led_on('blue')
        self.led_off('green')
        print("Working in OFFLINE-mode")

    def get_mode_online(self):
        return self.mode_online

    # saving sensor readings to DB. Checking if date is the same as when DB was initialized, otherwise re-initializes DB
    def save_sensor_readings(self, values):
        if self.sensor_readings_db_created != datetime.datetime.now().strftime('%d-%m-%y'):
            self.sensors_data = SensorReadingsData()
        time_stamp = datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')
        self.sensors_data.add_sensor_reading(time_stamp, self.VID, values)

    def led_on(self, color):
        leds = self.leds
        if len(leds) > 0:
            if leds.__contains__(color):
                leds[color].on()


    def led_off(self, color):
        leds = self.leds
        if len(leds) > 0:
            if leds.__contains__(color):
                leds[color].off()


    def add_to_db(self):
        devices_data = DevicesData()

        # devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280 Temperature Sensor', 'temperature', 'GPIO2, GPIO3, I2C: 0x77')
        # devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280 Humidity Sensor', 'humidity', 'GPIO2, GPIO3, I2C: 0x77')
        # devices_data.add_sensor('Adafruit_BME280', 'Adafruit_BME280l Pressure Sensor', 'pressure', 'GPIO2, GPIO3, I2C: 0x77')
        # devices_data.add_sensor('Adafruit_TCS34725', 'Adafruit_TCS34725 Light Sensor', 'light', 'I2C 0x29', False)

        # devices_data.add_output('led', 'LED Green', 'green', '26')
        # devices_data.add_output('led', 'LED Red', 'red', '13')
        # devices_data.add_output('console', 'Console Output', 'console', '')

        devices_data.add_sensor('virtual', 'Virtual Temperature Sensor', 'temperature', 'virtual')
        devices_data.add_sensor('humid_virt', 'Virtual Humidity Sensor', 'humidity', 'virtual')
        devices_data.add_sensor('gps_virt', 'Virtual GPS Sensor', 'gps', 'virtual')

        devices_data.close()

        # connected_to_SLN = False
        # SLN_current = None


# main = Main(SensorReadingsData())
main = Main()
main.start()




