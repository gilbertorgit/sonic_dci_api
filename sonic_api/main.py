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


class CreateSonicConfig:

    def __init__(self):
        self.SYSTEM = {}
        self.VRF = {}
        self.VLAN = {}
        self.LOOPBACK = {}
        self.PORTCHANNEL = {}
        self.INTERFACE = {}
        self.ROUTEMAP = {}
        self.BGP_GLOBAL = {}
        self.BGP_PG = {}
        self.BGP_NEIGH = {}
        self.BG_VNI_MAP = {}
        self.BGP_VRF = {}
        self.VTEP = {}

    @staticmethod
    def convertToList(string_name):

        li = list(string_name.split(","))
        return li

    def generateDataInfo(self, excel_file: str, tab_name: str):

        df = pd.read_excel(excel_file, sheet_name=tab_name)

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

        if tab_name == 'SYSTEM':
            self.SYSTEM = results
        elif tab_name == 'VRF':
            self.VRF = results
        elif tab_name == 'VLAN':
            self.VLAN = results
        elif tab_name == 'LOOPBACK':
            self.LOOPBACK = results
        elif tab_name == 'PORTCHANNEL':
            self.PORTCHANNEL = results
        elif tab_name == 'INTERFACE':
            self.INTERFACE = results
        elif tab_name == 'ROUTEMAP':
            self.ROUTEMAP = results
        elif tab_name == 'BGP_GLOBAL':
            self.BGP_GLOBAL = results
        elif tab_name == 'BGP_PG':
            self.BGP_PG = results
        elif tab_name == 'BGP_NEIGH':
            self.BGP_NEIGH = results
        elif tab_name == 'BGP_VNI_MAP':
            self.BGP_VNI_MAP = results
        elif tab_name == 'BGP_VRF':
            self.BGP_VRF = results
        elif tab_name == 'VTEP':
            self.VTEP = results

    def sendListInfo(self):

        excel_tab_list = ("SYSTEM", "VRF", "VLAN", "LOOPBACK", "PORTCHANNEL", "INTERFACE", "ROUTEMAP",
                          "BGP_GLOBAL", "BGP_PG", "BGP_NEIGH", "BGP_VNI_MAP", "BGP_VRF", "VTEP")

        for name in excel_tab_list:
            self.generateDataInfo('sonic_data.xlsx', name)

    def createSystemSonic(self):

        db = self.SYSTEM

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                hostname = db[i]['interface'][v]['hostname']
                interface_mode = db[i]['interface'][v]['interface_mode']
                port_group_id = db[i]['interface'][v]['port_group_id']
                anycast_mac = db[i]['interface'][v]['anycast_mac']
                anycast_ipv4 = db[i]['interface'][v]['anycast_ipv4']
                anycast_ipv6 = db[i]['interface'][v]['anycast_ipv6']
                instance = db[i]['interface'][v]['instance']

                a = Sonic()
    
                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }
                a.loginRequest(**connection_dict)
    
                a.hostnameConfigure(hostname)
                a.interfaceNamingModeConfigure(str(interface_mode).upper())
                for id in range(int(port_group_id)):
                    a.portGroupConfigure(id+1, "SPEED_10GB")
    
                if 'spine' not in hostname:
                    a.anyCastMacConfigure(anycast_mac, str(anycast_ipv4).lower(), str(anycast_ipv6).lower(), instance)

    def createVrfSonic(self):

        db = self.VRF

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

    def createVlanSonic(self):

        db = self.VLAN

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

    def createLoopbackSonic(self):

        db = self.LOOPBACK

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
                    # print(address, "com VRF instance")
                    a.loopBackBasicConfigure(loopback, enabled, description)
                    a.vrfInterfaceLoopBackAttachConfigure(loopback, instance)
                    a.ipv4InterfaceAddressConfigure(loopback, ip_address, prefix)

    def createPortchannelSonic(self):

        db = self.PORTCHANNEL

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

    def createInterfaceSonic(self):

        db = self.INTERFACE

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

    def createRouteMapSonic(self):

        db = self.ROUTEMAP

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                name = str(db[i]['interface'][v]['name'])
                policy_result = db[i]['interface'][v]['policy_result']
                as_number = db[i]['interface'][v]['as_number']
                sequence_number = db[i]['interface'][v]['sequence_number']
                match_set = str(db[i]['interface'][v]['match_set'])

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                a.rpPrependMcLagPeerConfigure(name, str(policy_result).upper(), int(as_number),
                                              int(sequence_number), str(match_set).upper())

    def createBgpGlobalSonic(self):

        db = self.BGP_GLOBAL

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                as_number = db[i]['interface'][v]['as_number']
                router_id = db[i]['interface'][v]['router_id']
                maximum_paths = db[i]['interface'][v]['maximum_paths']
                instance = db[i]['interface'][v]['instance']

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                if as_number != 'None' and router_id != 'None':
                    a.bgpGlobalConfigure(as_number, router_id, int(maximum_paths))
                    a.redistributeConnectedIpv4DefaultConfigure(instance)

    def createBgpPeerGroup(self):

        db = self.BGP_GLOBAL

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                peer_group = db[i]['interface'][v]['peer_group']
                export_policy = db[i]['interface'][v]['export_policy']
                source_ip = db[i]['interface'][v]['source_ip']

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                if peer_group != 'None':
                    if peer_group == 'fabric-underlay':
                        a.bgpPeerGroupUnderlayConfigure(peer_group)
                    elif peer_group == 'fabric-overlay':
                        a.bgpPeerGroupOverlayConfigure(peer_group, source_ip)
                    elif peer_group == 'mclag-peer':
                        a.bgpPeerGroupMcLagConfigure(peer_group, export_policy)

    def createBgpNeighbor(self):

        db = self.BGP_NEIGH

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                peer_address = db[i]['interface'][v]['peer_address']
                peer_as = db[i]['interface'][v]['peer_as']
                peer_group = db[i]['interface'][v]['peer_group']
                description = db[i]['interface'][v]['description']

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                if peer_address != 'None' and peer_as != 'None':
                    a.bgpNeighborConfigure(peer_address, int(peer_as), peer_group, description)

    def createBgpVniMap(self):

        db = self.BGP_VNI_MAP

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                instance = db[i]['interface'][v]['instance']
                vni = db[i]['interface'][v]['vni']
                rd_number = db[i]['interface'][v]['rd_number']
                rt_export = db[i]['interface'][v]['rt_export']
                rt_import = db[i]['interface'][v]['rt_import']

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                if vni != 'None' and instance != 'None':
                    a.bgpL2vpnVniMappingConfigure(instance, int(vni), rd_number, rt_import, rt_export)

    def createBgpVrf(self):

        db = self.BGP_VRF

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                as_number = db[i]['interface'][v]['as_number']
                router_id = db[i]['interface'][v]['router_id']
                rd_number = db[i]['interface'][v]['rd_number']
                rt_export = db[i]['interface'][v]['rt_export']
                rt_import = db[i]['interface'][v]['rt_import']
                instance = db[i]['interface'][v]['instance']
                peer_group = self.convertToList(db[i]['interface'][v]['peer_group'])

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                if as_number != 'None' and instance != 'None':
                    a.vrfBgpGlobalConfigure(int(as_number), router_id, rd_number, rt_export, rt_import, instance)
                    a.vrfRedistributeConnectedIpv4DefaultConfigure(instance)

                    if peer_group != None:
                        for pg_name in peer_group:
                            if pg_name == 'mclag-peer':
                                a.vrfBgpPeerGroupMcLagPeerConfigure(pg_name, instance)
                            elif pg_name == 'l3rtr':
                                a.vrfBgpPeerGroupL3rtrConfigure(pg_name, instance)

    def createVtepSonic(self):

        db = self.VTEP

        for i in db.keys():
            address = i
            for v in range(len(db[i]['interface'])):

                vtep_name = db[i]['interface'][v]['vtep_name']
                source_ip = db[i]['interface'][v]['source_ip']
                external_ip = db[i]['interface'][v]['external_ip']
                vni = db[i]['interface'][v]['vni']
                vlan = db[i]['interface'][v]['vlan']
                instance = db[i]['interface'][v]['instance']
                vni_vrf = db[i]['interface'][v]['vni_vrf']

                a = Sonic()

                connection_dict = {
                    'username': 'admin',
                    'password': 'admin',
                    'address': address,
                    'port': '443'
                }

                a.loginRequest(**connection_dict)

                if vtep_name != 'None' and source_ip != 'None':
                    # print("creating vtep interface", vtep_name, source_ip)
                    a.vTepVxLanInterfaceConfigure(vtep_name, source_ip)

                elif vtep_name != 'None' and vni != 'None' and vlan != 'None':
                    # print("creating vni vlan map", vtep_name, int(vni), int(vlan))
                    a.vTepVxLanVniMapConfigure(vtep_name, int(vni), str(int(vlan)))

                elif instance != 'None' and vni_vrf != 'None':
                    # print("creating vni vrf", instance, int(vni_vrf))
                    a.vrfVniMapConfigure(instance, int(vni_vrf))

    def saveConfigSonic(self):

        db = self.LOOPBACK

        for i in db.keys():
            address = i

            a = Sonic()

            connection_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': address,
                'port': '443'
            }

            a.loginRequest(**connection_dict)

            a.writeMemorySonic()


if __name__ == "__main__":

    sonic_instance = CreateSonicConfig()
    sonic_instance.sendListInfo()

    #sonic_instance.createSystemSonic()
    #sonic_instance.createVrfSonic()
    #sonic_instance.createVlanSonic()
    #sonic_instance.createLoopbackSonic()
    #sonic_instance.createPortchannelSonic()
    #sonic_instance.createInterfaceSonic()
    #sonic_instance.createRouteMapSonic()
    #sonic_instance.createBgpGlobalSonic()
    #sonic_instance.createBgpPeerGroup()
    #sonic_instance.createBgpNeighbor()
    #sonic_instance.createBgpVniMap()
    #sonic_instance.createBgpVrf()
    #sonic_instance.createVtepSonic()
    sonic_instance.saveConfigSonic()

