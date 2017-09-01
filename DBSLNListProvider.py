# Provides data model for SLNs
# Uses Peewee ORM for SQLite access

from peewee import *

# TODO: choose right .db file depending on the date

db = SqliteDatabase("db/roaming.db")

class Online_Slns(Model):
    id = CharField()
    addr = CharField()
    portNum = IntegerField()

    class Meta:
        database = db


class SLNListData(object):
    def __init__(self):
        db.connect()
        db.create_tables([Online_Slns], safe=True)
        # print("table created" + SensorData)

    def get_sln_list(self):
        return Online_Slns.select()



    def close(self):
        db.close()
