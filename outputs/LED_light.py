from gpiozero import LED

from outputs import Output


class LED_light(Output.Output):

    def __init__(self, name, full_name, type, connection=None):
        self.name = name
        self.full_name = full_name
        self.type = type
        self.connection = connection
        self.led = LED(int(self.connection))

    def on(self):
        self.led.on()
        # print("ON for ",self.led)

    def off(self):
        self.led.off()
        # print("OFF for ",self.led)

    def show_data(self):
        pass

    # def print_data(self):
    #     print(self.get_data())
    #
    # def save_data_to_sqlite(self):
    #     db_engine = DBSensorReadingsProvider()
    #     value = self.get_data()
    #     db_engine.add_sensor_reading(date, sensorName = self.name, value)


