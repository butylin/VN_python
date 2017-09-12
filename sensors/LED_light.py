from sensors import Output
import SensorDataProvidersFactory
import DBSensorReadingsProvider
from gpiozero import LED

class LED_light(Output.Output):

    def __init__(self, name, full_name, type, connection=None):
        self.name = name
        self.full_name = full_name
        self.type = type
        self.connection = connection

    def on(self):
        led = LED(self.connection)
        led.on()

    def off(self):
        pass

    def show_data(self):
        pass

    # def print_data(self):
    #     print(self.get_data())
    #
    # def save_data_to_sqlite(self):
    #     db_engine = DBSensorReadingsProvider()
    #     value = self.get_data()
    #     db_engine.add_sensor_reading(date, sensorName = self.name, value)


