import threading
import time
import random
import subprocess
import re


class Pinger():

    result = {}
    def ping(site):
        # sleep_time = random.randint(1, 5)
        # print("Pinging site: {} with sleep {}".format(site, sleep_time))
        # time.sleep(sleep_time)
        # print("Finished pinging site: ", site)
        # print("SLN ID: {}, SLN address: {}, SLN port: {}".format(sln.id, sln.addr, sln. portNum))

        # TODO: check if ping failed
        print("Pinging ", site)
        ping_str = site + " -c 4 -W 1"
        p = subprocess.Popen(["ping", "-c6", "-w100 ", site], stdout = subprocess.PIPE)
        ping_res = str(p.communicate()[0]).split('\\r\\n')

        ping = 0
        # parse string Reply from 54.239.17.6: bytes=32 time=39ms TTL=230
        for i in range(2, 6):
             ping += int(re.search('.*time=(.*)ms TTL=.*', ping_res[i]).group(1))
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

        print("FINISHED!")
        return Pinger.result


result = Pinger.ping_sites(['ya.ru', 'google.com', 'amazon.com', 'vet.tomsk.ru'])
print(result)