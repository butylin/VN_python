# Provides data model for sensor readings
# Responsible for using the right .db file depending on a date
# Uses Peewee ORM for SQLite access

from peewee import *

# TODO: choose right .db file depending on the date

db = SqliteDatabase("db/sensor_readings.db")

class SensorData(Model):
    time = DateTimeField()
    name = CharField()
    value = CharField()

    class Meta:
        database = db


class SensorReadingsData(object):
    def __init__(self):
        db.connect()
        db.create_tables([SensorData], safe=True)
        # print("table created" + SensorData)

    @classmethod
    def add_sensor_reading(self, date, sensorName, value):
        SensorData.get_or_create(time=date, name=sensorName, value=value)
        print("row added {1} : {2} : {3}".format(date, sensorName, value))

    def get_sensor_data_from_past_seconds(self, seconds):
        # TODO: selection by seconds
        SensorData.select()

    def close(self):
        db.close()
