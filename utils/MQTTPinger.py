import paho.mqtt.client as mqtt
import time, datetime
import threading

# gets list of servers and initializes MQTT connection to each of server.
# returns dictionary {server, connect time in microseconds}


class MQTTPinger():

    def __init__(self, config=None):
        # self.broker_list = broker_list
        self.config = config
        self.result = {}
        self.VIN = '77'
        self.ping_topic = '/roaming/control/' + self.VIN

    # gets time difference between time before connect and after connecting to broker
    def on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code "+str(rc))
        # TODO: find other solution to get times
        start_time = self.result[userdata]
        end_time = datetime.datetime.now().microsecond
        time_diff = end_time - start_time
        print("Server: {} Diff: {} Start: {} End: {} ".format(userdata, time_diff, start_time, end_time))
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
            # self.result[broker] = 'unknown'

    # iterates through brokers-list and calls 'ping_broker()' for every broker-address in sparate thread
    def ping_brokers(self, broker_list):
        threads = []
        for broker in broker_list:
            pingThread = threading.Thread(target=self.ping_broker, args=(broker, self.ping_topic))
            print("Pinging: ", broker)
            pingThread.start()
            # storing all started threads
            threads.append(pingThread)

        for t in threads:
            # waiting for all started threads to end
            t.join()

        # after all threads are finished returns class attribute 'result' which was used by threads
        return self.result

    #returns server with lowest connect_time as tuple (server, connect_time)
    def get_fastest(self, broker_list):
        latencys = self.ping_brokers(broker_list)
        if(not len(latencys) == 0):
            print(latencys)
            fastest = min(latencys, key=latencys.get)
            return fastest, latencys[fastest]
        else:
            return 0

# Server: 74.208.85.110 Diff: -829327 Start: 850730 End: 21403
# Server: test.mosquitto.org Diff: -789334 Start: 866885 End: 77551
# Server: butylin-aws.ddns.net Diff: -789272 Start: 868873 End: 79601



# list = ['test.mosquitto.org', 'butylin-aws.ddns.net', '74.208.85.110']
        # pinger = MQTTPinger()
        # print(pinger.ping_brokers(list))