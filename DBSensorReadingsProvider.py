# Provides data model for sensor readings
# Responsible for using the right .db file depending on a date
# Uses Peewee ORM for SQLite access

from peewee import *
from datetime import datetime
from time import sleep
import random

DB_FILE_FOLDER = 'db'
DB_FILE_NAME = 'sensor_readings'

# db-file name is set dynamically in SensorReadingsData constructor
db = SqliteDatabase(None)

class SensorData(Model):
    time = DateTimeField()
    vid = IntegerField()
    sensor_data = CharField()

    class Meta:
        database = db


class SensorReadingsData(object):
    def __init__(self):
        date_stamp = datetime.now().strftime('_%d-%m-%y')
        # form a DB-file name for current day
        db_file = DB_FILE_FOLDER + '/' + DB_FILE_NAME + date_stamp + '.db'
        db.init(db_file)
        db.connect()
        db.create_tables([SensorData], safe=True)
        print(db)

    @classmethod
    def add_sensor_reading(self, time, vid, sensor_data):
        SensorData.get_or_create(time=time, vid=vid, sensor_data=sensor_data)
        print("row added {} : {} : {}".format(time, vid, sensor_data))

    def get_sensor_data_from_past_seconds(self, seconds):
        # TODO: selection by seconds
        SensorData.select()

    def close(self):
        db.close()
        print("db closed")


# class SensorData(Model):
#     time = DateTimeField()
#     name = CharField()
#     value = CharField()
#
#     class Meta:
#         database = db
#
#
# class SensorReadingsData(object):
#     def __init__(self):
#         date_stamp = datetime.now().strftime('_%d-%m-%y')
#         # form a DB-file name for current day
#         db_file = DB_FILE_FOLDER + '/' + DB_FILE_NAME + date_stamp + '.db'
#         db.init(db_file)
#         db.connect()
#         db.create_tables([SensorData], safe=True)
#         print(db)
#
#     @classmethod
#     def add_sensor_reading(self, date, sensorName, value):
#         SensorData.get_or_create(time=date, name=sensorName, value=value)
#         print("row added {} : {} : {}".format(date, sensorName, value))
#
#     def get_sensor_data_from_past_seconds(self, seconds):
#         # TODO: selection by seconds
#         SensorData.select()
#
#     def close(self):
#         db.close()
#         print("db closed")


