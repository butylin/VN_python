import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time
import threading

class MQTTPinger():
    result = {}
    VIN = '77'
    ping_topic = '/control/roaming/ping/'

    @staticmethod
    def on_connect(self, client, userdata, flags, rc):


    @staticmethod
    def ping_broker(broker, topic):
        latency_mlsec = 0
        mqtt_client = mqtt.Client()
        sub_topic = MQTTPinger.ping_topic + MQTTPinger.VIN
        mqtt_client.on_connect = MQTTPinger.on_connect
        mqtt_client.subscribe(sub_topic)
        MQTTPinger.result[broker] = 0
        mqtt_client.connect(broker, 1883, 60)

    @staticmethod
    def ping_brokers(brokers_list, ping_topic):
        threads = []
        for broker in brokers_list:
            pingThread = threading.Thread(target=MQTTPinger.ping_broker(), args=(broker, ping_topic))
            pingThread.start()
            threads.append(pingThread)

        for t in threads:
            t.join()