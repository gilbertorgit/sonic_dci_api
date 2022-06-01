"""
---------------------------------
 Author: Gilberto Rampini
 Date: 07/2022
---------------------------------
"""

import pandas as pd
import openpyxl
from base_sonic import *


def read_excel_data(file, sheet_name):
    db = pd.read_excel(file, sheet_name=sheet_name)
    return db


def getSystemTab(file, sheet_name):

    db = read_excel_data(file, sheet_name)

    dc_dict = {}
    for i in range(len(db["mgmt_ip"])):
        if db["mgmt_ip"][i] != 0:
            mgmt_ip = db["mgmt_ip"][i]
            dc_dict[mgmt_ip] = {}
        else:
            hostname = db["hostname"][i]
            interface_mode = db["interface_mode"][i]
            port_group_id = db["port_group_id"][i]
            anycast_mac = db["anycast_mac"][i]
            anycast_ipv4 = db["anycast_ipv4"][i]
            anycast_ipv6 = db["anycast_ipv6"][i]
            instance = db["instance"][i]

            dc_dict[mgmt_ip]['hostname'] = hostname
            dc_dict[mgmt_ip]['interface_mode'] = str(interface_mode).upper()
            dc_dict[mgmt_ip]['port_group_id'] = int(port_group_id)
            dc_dict[mgmt_ip]['anycast_mac'] = anycast_mac
            dc_dict[mgmt_ip]['anycast_ipv4'] = str(anycast_ipv4).lower()
            dc_dict[mgmt_ip]['anycast_ipv6'] = str(anycast_ipv6).lower()
            dc_dict[mgmt_ip]['instance'] = instance

    return dc_dict


if __name__ == "__main__":

    def create_system_sonic():

        db = getSystemTab('sonic_data.xlsx', sheet_name='SYSTEM')

        for i in db.keys():

            address = i
            hostname = db[i].get('hostname')
            interface_mode = db[i].get('interface_mode')
            port_group_id = db[i].get('port_group_id')
            anycast_mac = db[i].get('anycast_mac')
            anycast_ipv4 = db[i].get('anycast_ipv4')
            anycast_ipv6 = db[i].get('anycast_ipv6')
            instance = db[i].get('instance')

            a = Sonic()

            test_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }
            a.loginRequest(**test_dict)

            a.hostnameConfigure(hostname)
            a.interfaceNamingModeConfigure(interface_mode)
            for id in range(port_group_id):
                a.portGroupConfigure(id+1, "SPEED_10GB")

            if 'spine' not in hostname:
                a.anyCastMacConfigure(anycast_mac, anycast_ipv4, anycast_ipv6, instance)


    create_system_sonic()