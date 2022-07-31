"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""
import os
import time
from time import sleep
import console_config
from basicInfra import *
import threading
from itertools import islice


class ConfigureRouter(threading.Thread):
    def __init__(self, hostname, virtual_image, mgmt_ip=None):
        threading.Thread.__init__(self)
        self.mgmt_ip = mgmt_ip
        self.hostname = hostname
        self.virtual_image = virtual_image

    def run(self):

        if self.virtual_image == 'sonic':
            if self.mgmt_ip is None:
                console_config.config_virtual_sonic_ztp(self.hostname)


def configure_sonic_ztp():

    threads = []

    print("Wait 2 minutes to disable Sonic ZTP")
    start_time = time.time()
    sleep(120)
    run_time = time.time() - start_time
    print("** Time waiting: %s sec" % round(run_time, 2))
    print("########## Basic MGMT Configuration - hostname and ip")

    a = BasicInfra()
    virtual_hosts = a.createVirtualVmDic("vrdc_info.csv")

    """
    for i in virtual_hosts.keys():
        hostname = virtual_hosts[i].get('hostname')

        thread = ConfigureRouter(hostname=hostname, virtual_image='sonic')
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    """

    for i in virtual_hosts.keys():
        hostname = virtual_hosts[i].get('hostname')

        console_config.config_virtual_sonic_ztp(hostname)


def configure_virtual_router():

    print("Wait 4 minutes to start MGMT configuration")
    sleep(240)
    print("########## Basic MGMT Configuration - hostname and ip")

    a = BasicInfra()
    virtual_hosts = a.createVirtualVmDic("vrdc_info.csv")

    for i in virtual_hosts.keys():
        hostname = virtual_hosts[i].get('hostname')
        mgmt_ip = virtual_hosts[i].get('mgmt_ip')

        console_config.config_virtual_sonic(hostname, mgmt_ip)


def check_ping():

    a = BasicInfra()
    virtual_hosts = a.createVirtualVmDic("vrdc_info.csv")

    for i in virtual_hosts.keys():
        hostname = virtual_hosts[i].get('hostname')
        mgmt_ip = virtual_hosts[i].get('mgmt_ip')

        response = os.system("ping -c 1 " + mgmt_ip)

        if response == 0:
            pingstatus = print(f'{hostname} - MGMT Network: {mgmt_ip} is reachable')
        else:
            pingstatus = print(f'{hostname} - MGMT Network: {mgmt_ip} is unreachable')

        return pingstatus

if __name__ == "__main__":
    check_ping()