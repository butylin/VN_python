import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time, datetime
import threading


class MQTTPinger():

    def __init__(self, broker_list, config=None):
        self.broker_list = broker_list
        self.config = config
        self.result = {}
        self.VIN = '77'
        self.ping_topic = '/roaming/control/' + self.VIN

    def on_connect(self, client, userdata, flags, rc):

        print("connected")

        # now = datetime.datetime.now().microsecond
        # print("Server {} start {} end {}: ".format(userdata, self.result[userdata], now))
        # time_diff = datetime.datetime.now().microsecond - self.result[userdata]
        # self.result[userdata] = time_diff;
        #
        # client.disconnect()

    def ping_broker(self, broker, topic):
        mqtt_client = mqtt.Client(userdata=broker)
        mqtt_client.on_connect = self.on_connect
        print("client ", mqtt_client.on_connect)
        # mqtt_client.subscribe(sub_topic)
        self.result[broker] = datetime.datetime.now().microsecond
        mqtt_client.connect(broker, 1883, 10)
        # mqtt_client.loop_start()

    def ping_brokers(self):
        threads = []
        for broker in self.broker_list:
            pingThread = threading.Thread(target=self.ping_broker, args=(broker, self.ping_topic))
            print("Starting thread: ", pingThread)
            pingThread.start()
            threads.append(pingThread)

        for t in threads:
            t.join()

        return self.result

list = ['test.mosquitto.org', 'butylin-aws].ddns.net', '74.208.85.110']
pinger = MQTTPinger(list)
print(pinger.ping_brokers())