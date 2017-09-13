import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from DBSLNListProvider import SLNListData
from time import sleep
import os
import subprocess
from utils import Pinger
from utils import MQTTPinger

MQTT_ROAMING_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_VID = '77'
MQTT_TOPIC = "/control/roaming"
DB_FILE_ROAMING = "db/roaming.db"
# FLAG_DB_CREATED = False
CONNECTION_TIMEOUT = 10

class MQTTHandshakeHandler:
    FLAG_DB_CREATED = False
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected to Roaming MQTT broker. Code: "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC + "/" + MQTT_VID)
        print("Subscribing")
        client.publish(MQTT_TOPIC, MQTT_VID)
        print('Publishing to: {} msg: {}'.format(MQTT_TOPIC, MQTT_VID))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print("Recieved message from {}\nMessage content: {}".format(msg.topic, str(msg.payload)))
        if self.make_db_file(msg.payload):
            self.FLAG_DB_CREATED = True

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

    # Delete roaming SLN-db file
    def delete_sln_db(self):
        os.remove(DB_FILE_ROAMING)
        self.FLAG_DB_CREATED = False
        print("DB-file deleted: ", DB_FILE_ROAMING)

    def do_handshake(self, conf=None, sln_db=None, client=None):
        if client is None:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            try:
                client.connect_async(MQTT_ROAMING_SERVER, MQTT_PORT, MQTT_ALIVE)
                client.loop_start()
            except Exception as e:
                print("Unable to connect to roaming server {} -- {}".format(MQTT_ROAMING_SERVER, e))
                return -1
        if sln_db is None:
            sln_db = SLNListData()



        # sending Vehicle ID to a roaming server and waiting for a response with SLN-list (listening for a roaming topic)
        # client.publish(MQTT_TOPIC, MQTT_VID)
        # print('Publishing to: {} msg: {}'.format(MQTT_TOPIC, MQTT_VID))

        print("Waiting for list of SLNs from Roaming Node", MQTT_TOPIC)

        timer = 10
        #wait for MQTT message for 'timer' seconds
        while (not self.FLAG_DB_CREATED) and (timer > 0):
            print(timer)
            timer -= 1
            sleep(1)

        if not self.FLAG_DB_CREATED:
            print("Haven't received SLN-list from roaming server. Trying connection again")
            # sln_db.close()
            self.do_handshake(sln_db, client)
        else:
            sln_list = sln_db.get_sln_list()
            print(sln_list)


            # finding fasted SLN
            if not len(sln_list) == 0:
                sites = []
                for sln in sln_list:
                    print(sln.addr)
                    sites.append(sln.addr)
            else:
                print("No online SLNs in the area")
                return -1

            # best_sln = Pinger.Pinger.ping_sites(sites)
            pinger = MQTTPinger.MQTTPinger()

            best_sln = pinger.get_fastest(sites)

            print("Best server: ", best_sln)

        if self.FLAG_DB_CREATED:
            sln_db.close()
            self.delete_sln_db()

        return best_sln

# sub = MQTTHandshakeHandler()
# sub.do_handshake()