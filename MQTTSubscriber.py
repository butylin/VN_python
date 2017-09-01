import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from DBSLNListProvider import SLNListData
from time import sleep
import os
import subprocess

MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "/control/roaming/77"
DB_FILE_ROAMING = "db/roaming.db"
FLAG_DB_CREATED = False
CONNECTION_TIMEOUT = 10

class MQTTSubscriber:
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print("Recieved message from {}\nMessage content: {}".format(msg.topic, str(msg.payload)))
        if(self.make_db_file(msg.payload)):
            global FLAG_DB_CREATED
            FLAG_DB_CREATED = True

    # creates DB-file from MQTT message bytes
    def make_db_file(self, content):
        try:
            # create/open file as binary file
            file = open(DB_FILE_ROAMING, "wb")
        except Exception as e:
            print("Cannot open/create DB file: ", e)
            return False
        try:
            file.write(content)
        except Exception as e:
            print("Cannot write content to db-file: ", e)
            return False

        print("DB-file created: ", file.name)
        return True

    def delete_sln_db(self):
        os.remove(DB_FILE_ROAMING)
        print("DB-file deleted: ", DB_FILE_ROAMING)

    def main(self, sln_db=None, client=None):
        if client == None:
            client = mqtt.Client()
        if sln_db == None:
            sln_db = SLNListData()

        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect_async(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
        client.loop_start()


        print("Waiting for list of SLNs from Roaming Node", MQTT_TOPIC)


        timer = 10
        #wait for MQTT message
        while not FLAG_DB_CREATED and (timer > 0):
            print(timer)
            timer -= 1
            sleep(1)

        if not FLAG_DB_CREATED:
            print("No SLN db was not created. Trying again")
            # sln_db.close()
            self.main(sln_db, client)
        else:
            sln_list = sln_db.get_sln_list()
            print(sln_list)

            for sln in sln_list:
                print("SLN ID: {}, SLN address: {}, SLN port: {}".format(sln.id, sln.addr, sln. portNum))
                p = subprocess.Popen(["ping",sln.addr], stdout = subprocess.PIPE)
                print(p.communicate()[0])

        # finding fasted SLN



        sln_db.close()
        self.delete_sln_db()






sub = MQTTSubscriber()
sub.main()