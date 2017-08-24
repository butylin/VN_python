import sqlite3
import random
import time, datetime
import os

DB_TABLE_EVENTS = "events"
DB_KEY_TIME = "time"
DB_KEY_TEMPERATURE = "temperature"
DB_FOLDER = "db"
DB_FILE_NAME_FORMAT = "%Y%m%d-%H"
DB_CONNECTION = None
db_connected = False


# returns tuples (current_time, current_temperature)
def generateData():
    temp_avg = 50
    temp_increase = random.randint(0,20)
    curr_time = str(datetime.datetime.now())
    curr_temp = temp_avg + temp_increase
    values = (curr_time, curr_temp)
    return values

# return connection to DB
# checks if there is a DB-file for current hour, if not creates file and DB-table
# returns cursor for current DB-file
def getDBConnection():
    global DB_CONNECTION
    # db_connection = DB_CONNECTION
    curr_db_file = currentDBFile()
    #
    print('Initializing connection to DB..')
    print('Current DB-file name: ' + curr_db_file)
    #
    if os.path.isfile(curr_db_file):
        print(curr_db_file + ' DB-file exists')
        if DB_CONNECTION != None:
            print("Connection already established...")
            return DB_CONNECTION
        else:
            try:
                DB_CONNECTION = sqlite3.connect(curr_db_file)
                #
                print('New connection initiated to ' + curr_db_file)
                #
                return DB_CONNECTION
            except Exception as e:
                print(e)
    else:
        print(curr_db_file + ' DB-file doesnt exists')
        if DB_CONNECTION != None:
            try:
                DB_CONNECTION.close
                print('Old connection closed succesfully...')
                DB_CONNECTION = sqlite3.connect(curr_db_file)
                print('New file connection initiated to ' + curr_db_file)
                db_cur = DB_CONNECTION.cursor()
                db_cur.execute('CREATE TABLE {} ({}, {})'.format(DB_TABLE_EVENTS, DB_KEY_TIME, DB_KEY_TEMPERATURE))
                DB_CONNECTION.commit()
                print('Table created: ' + DB_TABLE_EVENTS)
                db_cur.close()
                return DB_CONNECTION
            except Exception as e:
                print(e)
        else:
            try:
                DB_CONNECTION = sqlite3.connect(curr_db_file)
                print('New file created and connection initiated to ' + curr_db_file)
                db_cur = DB_CONNECTION.cursor()
                db_cur.execute('CREATE TABLE {} ({}, {})'.format(DB_TABLE_EVENTS, DB_KEY_TIME, DB_KEY_TEMPERATURE))
                DB_CONNECTION.commit()
                db_cur.close()
                return DB_CONNECTION
            except Exception as e:
                print(e)


# checks if DB-file for current hour exists
def currentDBFile():
    curr_time = time.strftime(DB_FILE_NAME_FORMAT)
    curr_db_file = DB_FOLDER + "/" + curr_time + ".db"
    return curr_db_file


def streamDataIntoDB():
    while(True):
        values = generateData()
        print('Values generated: ' + str(values))
        try:
            db_connection = getDBConnection()
            db_cur = db_connection.cursor()
            db_cur.execute('INSERT INTO ' + DB_TABLE_EVENTS + ' VALUES (?, ?)', values)
            db_connection.commit()
            print('Values inserted')
            time.sleep(1)
        except KeyboardInterrupt as e:
            print("Interrupted")
            db_connection.rollback
            db_connection.close
            break
        except Exception as e:
            print(e)

        print('*********************************************')


streamDataIntoDB()




