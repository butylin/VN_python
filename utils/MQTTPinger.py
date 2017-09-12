import paho.mqtt.client as mqtt
import time, datetime
import threading

# gets list of servers and initializes MQTT connection to each of server.
# returns dictionary {server, connect time in microseconds}


class MQTTPinger():

    def __init__(self, broker_list, config=None):
        self.broker_list = broker_list
        self.config = config
        self.result = {}
        self.VIN = '77'
        self.ping_topic = '/roaming/control/' + self.VIN

    # gets time difference between time before connect and after connecting to broker
    def on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code "+str(rc))
        start_time = self.result[userdata]
        end_time = datetime.datetime.now().microsecond
        time_diff = end_time - start_time
        # print("Server {} timediff {} start {} end {}: ".format(userdata, time_diff, start_time, end_time))
        self.result[userdata] = time_diff
        client.disconnect()

    # creates connection to a mqtt-broker, sends broker address as 'userdata' attribute
    def ping_broker(self, broker, topic):
        mqtt_client = mqtt.Client(userdata=broker)
        mqtt_client.on_connect = self.on_connect
        self.result[broker] = datetime.datetime.now().microsecond
        try:
            mqtt_client.connect(broker, 1883, 5)
            mqtt_client.loop_forever()
        except Exception as e:
            print("Error connecting to {} -- {}".format(broker, e))
            self.result[broker] = -1

    # iterates through brokers-list and calls 'ping_broker()' for every broker-address in sparate thread
    def ping_brokers(self):
        threads = []
        for broker in self.broker_list:
            pingThread = threading.Thread(target=self.ping_broker, args=(broker, self.ping_topic))
            print("Starting thread: ", pingThread)
            pingThread.start()
            # storing all started threads
            threads.append(pingThread)

        for t in threads:
            # waiting for all started threads to end
            t.join()

        return self.result


# list = ['test.mosquitto.org', 'butylin-aws.ddns.net', '74.208.85.11', 'bumbum.com']
# pinger = MQTTPinger(list)
# print(pinger.ping_brokers())