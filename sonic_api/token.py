"""
---------------------------------
 Author: Gilberto Rampini
 Date: 07/2022
---------------------------------
"""

import pandas as pd
import json
import numpy as np
import openpyxl
from base_sonic import *


def read_excel_data(file, sheet_name):
    db = pd.read_excel(file, sheet_name=sheet_name)
    return db


def fileReadExcel(file, sheet_name):

    df = pd.read_excel(file, sheet_name)
    df['mgmt_ip'] = df['mgmt_ip'].replace({0: np.nan}).fillna(method='ffill')
    df = df.replace({None: np.nan})
    df = df.dropna(thresh=2)
    df = df.fillna('None')


    results = {}
    for name, g in df.groupby(by=['mgmt_ip']):
        g = g.drop('mgmt_ip', axis=1)
        data = json.loads(g.to_json(orient='table'))['data']
        for d in data:
            __ = d.pop('index')
        results[name] = {
            'interface': data
        }
    return results


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

        connection_dict = {
            'username': 'admin',
            'password': 'admin',
            'address': address,
            'port': '443'
        }
        a.loginRequest(**connection_dict)

        a.hostnameConfigure(hostname)
        a.interfaceNamingModeConfigure(interface_mode)
        for id in range(port_group_id):
            a.portGroupConfigure(id+1, "SPEED_10GB")

        if 'spine' not in hostname:
            a.anyCastMacConfigure(anycast_mac, anycast_ipv4, anycast_ipv6, instance)


def getVlanTab():

    df = pd.read_excel('sonic_data.xlsx', sheet_name='VLAN')
    df['mgmt_ip'] = df['mgmt_ip'].replace({0: np.nan}).fillna(method='ffill')
    df = df.replace({None: np.nan})
    df = df.dropna(thresh=2)
    df = df.fillna('None')


    results = {}
    for name, g in df.groupby(by=['mgmt_ip']):
        g = g.drop('mgmt_ip', axis=1)
        data = json.loads(g.to_json(orient='table'))['data']
        for d in data:
            __ = d.pop('index')
        results[name] = {
            'interface': data
        }

    return results


def getLoopbackTab():

    df = pd.read_excel('sonic_data.xlsx', sheet_name='LOOPBACK')
    df['mgmt_ip'] = df['mgmt_ip'].replace({0: np.nan}).fillna(method='ffill')
    df = df.replace({None: np.nan})
    df = df.dropna(thresh=2)
    df = df.fillna('None')


    results = {}
    for name, g in df.groupby(by=['mgmt_ip']):
        g = g.drop('mgmt_ip', axis=1)
        data = json.loads(g.to_json(orient='table'))['data']
        for d in data:
            __ = d.pop('index')
        results[name] = {
            'interface': data
        }
    return results


def create_vrf_sonic(file, sheet_name):

    db = fileReadExcel(file, sheet_name)

    for i in db.keys():
        address = i
        for v in range(len(db[i]['interface'])):
            instance = str(db[i]['interface'][v]['instance'])

            a = Sonic()

            connection_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }

            a.loginRequest(**connection_dict)

            a.vrfConfigure(instance)


def create_vlan_sonic():

    db = getVlanTab()

    for i in db.keys():

        address = i
        for v in range(len(db[i]['interface'])):
            vlan = int(db[i]['interface'][v]['vlan'])
            mtu = int(db[i]['interface'][v]['mtu'])
            enabled = str(db[i]['interface'][v]['enabled']).lower()
            instance = str(db[i]['interface'][v]['instance'])
            description = db[i]['interface'][v]['description']
            anycast_ip = db[i]['interface'][v]['anycast_ip']

            a = Sonic()

            connection_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }
            a.loginRequest(**connection_dict)

            if anycast_ip == 'None':

                a.vlanBasicConfigure(vlan, mtu, enabled, description)
                a.arpSuppressConfigure(vlan)
                a.vrfInterfaceAttachConfigure(vlan, instance)

            else:
                a.vlanBasicConfigure(vlan, mtu, enabled, description)
                a.arpSuppressConfigure(vlan)
                a.vrfInterfaceAttachConfigure(vlan, instance)
                a.interfaceAnyCastGwConfigure(vlan, anycast_ip)


def create_loopback_sonic(file, sheet_name):

    db = fileReadExcel(file, sheet_name)
    print(db)

    for i in db.keys():
        address = i
        for v in range(len(db[i]['interface'])):
            loopback = str(db[i]['interface'][v]['loopback']).title()
            description = str(db[i]['interface'][v]['description'])
            instance = str(db[i]['interface'][v]['instance'])
            enabled = str(db[i]['interface'][v]['enabled']).lower()
            ip_address = str(db[i]['interface'][v]['ip_address'])
            prefix = int(db[i]['interface'][v]['prefix'])

            a = Sonic()

            connection_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }
            a.loginRequest(**connection_dict)

            if instance == 'None':
                a.loopBackBasicConfigure(loopback, enabled, description)
                a.ipv4InterfaceAddressConfigure(loopback, ip_address, prefix)
            else:
                print(address, "com VRF instance")
                a.loopBackBasicConfigure(loopback, enabled, description)
                a.vrfInterfaceLoopBackAttachConfigure(loopback, instance)
                a.ipv4InterfaceAddressConfigure(loopback, ip_address, prefix)


def create_portchannel_sonic(file, sheet_name):

    db = fileReadExcel(file, sheet_name)

    for i in db.keys():
        address = i
        for v in range(len(db[i]['interface'])):

            interface = str(db[i]['interface'][v]['interface'])
            mtu = db[i]['interface'][v]['mtu']
            enabled = str(db[i]['interface'][v]['enabled']).lower()
            description = str(db[i]['interface'][v]['description'])
            ip_address = str(db[i]['interface'][v]['ip_address'])
            prefix = db[i]['interface'][v]['prefix']
            access_vlan = db[i]['interface'][v]['access_vlan']
            tagged_vlan = str(db[i]['interface'][v]['tagged_vlan'])
            admin_status = str(db[i]['interface'][v]['admin_status'])
            mclag_domain = db[i]['interface'][v]['mclag_domain']
            mclag_interface = str(db[i]['interface'][v]['mclag_interface'])
            src_ip = str(db[i]['interface'][v]['src_ip'])
            dest_ip = str(db[i]['interface'][v]['dest_ip'])

            a = Sonic()

            connection_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }

            a.loginRequest(**connection_dict)

            if ip_address != 'None':
                #print(address, interface, "é vlan")
                a.vlanBasicConfigure(interface, int(mtu), enabled, description)
                a.mcLagSeparateIpConfigure(interface)
                a.vlanIpv4AddressConfigure(interface, ip_address, int(prefix))

            elif tagged_vlan != 'None' and access_vlan == 'None':
                #print(address, interface, "é portchannel do mclag")
                a.portChannelTaggedConfigure(interface, int(mtu), tagged_vlan, admin_status)

            elif src_ip != 'None' and dest_ip != 'None':
                #print(address, interface, "é mclag")
                a.mcLagConfigure(int(mclag_domain), src_ip, dest_ip, mclag_interface)

            elif access_vlan != 'None' and tagged_vlan == 'None':
                #print(address, interface, "é portchannel access")
                a.portChannelAccessConfigure(interface, int(mtu), int(access_vlan), admin_status)



def create_portchannel_sonic(file, sheet_name):

    db = fileReadExcel(file, sheet_name)

    for i in db.keys():
        address = i
        for v in range(len(db[i]['interface'])):

            interface = str(db[i]['interface'][v]['interface'])
            mtu = db[i]['interface'][v]['mtu']
            enabled = str(db[i]['interface'][v]['enabled']).lower()
            description = str(db[i]['interface'][v]['description'])
            ip_address = str(db[i]['interface'][v]['ip_address'])
            prefix = db[i]['interface'][v]['prefix']
            access_vlan = db[i]['interface'][v]['access_vlan']
            channel_group = db[i]['interface'][v]['channel_group']
            portchannel_interface = db[i]['interface'][v]['portchannel_interface']

            a = Sonic()

            connection_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }

            a.loginRequest(**connection_dict)

            if channel_group != 'None' and portchannel_interface != 'None' and mtu != 'None':
                # print("is portchannel interface")
                a.physicalIntBasicConfigure(interface, int(mtu), enabled, description)
                a.portChannelMemberConfigure(interface, portchannel_interface)

            elif ip_address != 'None' and prefix != 'None':
                # print("is ipv4 interface")
                a.interfaceIpv4FullConfigure(interface, ip_address, int(prefix), enabled, description)

            elif access_vlan != 'None' and ip_address == 'None':
                # print("is access interface")
                a.vlanAccessConfigure(interface, int(mtu), enabled, access_vlan)


if __name__ == "__main__":

    #create_system_sonic()
    #create_vrf_sonic('sonic_data.xlsx', sheet_name='VRF')
    #create_vlan_sonic()
    #create_loopback_sonic('sonic_data.xlsx', sheet_name='LOOPBACK')
    #create_portchannel_sonic('sonic_data.xlsx', sheet_name='PORTCHANNEL')
    create_portchannel_sonic('sonic_data.xlsx', sheet_name='INTERFACE')