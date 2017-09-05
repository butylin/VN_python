import threading
import time
import random
import subprocess
import re


class Pinger():

    result = {}

    @staticmethod
    def ping(site):
        # sleep_time = random.randint(1, 5)
        # print("Pinging site: {} with sleep {}".format(site, sleep_time))
        # time.sleep(sleep_time)
        # print("Finished pinging site: ", site)
        # print("SLN ID: {}, SLN address: {}, SLN port: {}".format(sln.id, sln.addr, sln. portNum))

        # TODO: check if ping failed
        print("Pinging ", site)
        # ping_str = site + " -c 5 -W 1"
        p = subprocess.Popen(["ping", "-c4", "-w100 ", site], stdout = subprocess.PIPE)
        ping_res = list((str(p.communicate()[0])).split('\n')) #linux format
        # ping_res = list((str(p.communicate()[0])).split('\\r\\n')) #windows format
        ping = 0

        for i in range(2, 5):
            ping += float(re.search('.*time=(.*) ms.*', ping_res[i]).group(1)) # parse linux ping string: 64 bytes from ya.ru (87.250.250.242): icmp_seq=1 ttl=44 time=151 ms
            # ping += float(re.search('.*time=(.*)ms TTL=.*', ping_res[i]).group(1)) # parse windows ping string: Reply from 87.250.250.242: bytes=32 time=154ms TTL=44
        Pinger.result[site] = ping/4

    @staticmethod
    def ping_sites(site_list):
        threads = []
        for site in site_list:
            t = threading.Thread(target=Pinger.ping, args=(site,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        fastest_key = min(Pinger.result, key=Pinger.result.get)
        # print("Fastest server: ", fastest_key, Pinger.result.get(fastest_key))

        return fastest_key, Pinger.result.get(fastest_key)



result = Pinger.ping_sites(['ya.ru', 'google.com', 'amazon.com', 'vet.tomsk.ru'])
print(result)