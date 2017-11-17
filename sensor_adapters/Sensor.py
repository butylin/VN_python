# import SensorDataProvidersFactory
# import DBSensorReadingsProvider

# Sensor interface
class Sensor:

    def __init__(self, name, full_name, sensor_type, connection = None, id=None):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.type = sensor_type
        self.connection = connection

    @classmethod
    def get_data(self):
        pass

    # def print_data(self):
    #     print(self.get_data())
    #
    # def save_data_to_sqlite(self):
    #     db_engine = DBSensorReadingsProvider()
    #     value = self.get_data()
    #     db_engine.add_sensor_reading(date, sensorName = self.name, value)