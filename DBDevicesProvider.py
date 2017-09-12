# Provides data model for list of sensor devices, list of output devices and sensor readings
# Uses Peewee ORM for SQLite access
from peewee import *
db = SqliteDatabase("db/devices.db")


class Sensor(Model):
    name = CharField()
    full_name = CharField()
    type = CharField()
    connection = CharField()
    active = BooleanField()

    class Meta:
        database = db


class Output(Model):
    name = CharField()
    full_name = CharField()
    type = CharField()
    connection = CharField()
    active = BooleanField()

    class Meta:
        database = db


class DevicesData(object):
    def __init__(self):
        db.connect()
        # @safe flag ensures existing table will not be overwritten
        db.create_tables([Sensor, Output], safe=True)
        # print("table created" + Sensor + " " + Output )

    def add_sensor(self, name, fullName, type, connection, active=True):
        Sensor.get_or_create(name=name, full_name=fullName, type=type, connection=connection, active=active)
        print("row added {} : {} : {} : {}".format(name, fullName, type, connection))

    def add_output(self, name, fullName, type, connection, active=True):
        Output.get_or_create(name=name, full_name=fullName, type=type, connection=connection, active=active)
        print("row added {} : {} : {} : {}".format(name, fullName, type, connection))

    def get_all_sensors(self):
        return Sensor.select()

    def get_all_outputs(self):
        return Output.select()

    def get_sensors_by_type(self, type):
        # TODO: type selection in peewee
        return Sensor.select()

    def get_outputs_by_type(self, type):
        # TODO: type selection in peewee
        return Output.select()

    def get_sensor_by_fullname(self, fullname):
        # TODO: fullname selection in peewee
        return Sensor.select()

    def get_outputs_by_fullname(self, fullname):
        # TODO: fullname selection in peewee
        return Output.select()

#     TODO: delete sensors


    def close(self):
        db.close
