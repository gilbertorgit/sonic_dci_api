"""
---------------------------------
 Author: Gilberto Rampini
 Date: 07/2022
---------------------------------
"""

import requests
import json
from interfaces_sonic import *
from system_sonic import *
from vrf_sonic import *
from routing_policy_sonic import *
from bgp_sonic import *

requests.packages.urllib3.disable_warnings() #Supress SSL verify warnings

class Sonic():

    def __init__(self):
        self.password = None
        self.username = None
        self.address = None
        self.port = None
        self.base_url = None
        self.api_token = None

        #Token URL
        self.url_token = '/authenticate'

        #Interfaces URL
        self.url_interface_all = '/restconf/data/openconfig-interfaces:interfaces/'

        #System URL
        self.url_system = '/restconf/data/openconfig-system:system'

        #Port Group URL
        self.url_portgroup = '/restconf/data/openconfig-port-group:port-groups'

        #Arp Suppress
        self.url_arp_suppress = '/restconf/data/sonic-vxlan:sonic-vxlan'

        #Network Instances - Protocols, VRF, default etc
        self.url_network_instances =  '/restconf/data/openconfig-network-instance:network-instances'
        self.url_network_instances_bgp = '/restconf/data/openconfig-network-instance:network-instances/network-instance=default/protocols/protocol=BGP,bgp/'

        #VRF Sonic Url
        self.url_vrf_sonic = '/restconf/data/sonic-vrf:sonic-vrf'

        #PortChannel Sonic URL
        self.url_portchannel_int = '/restconf/data/sonic-portchannel:sonic-portchannel'

        #MCLAG Sonic URL
        self.url_mclag_sonic = '/restconf/data/sonic-mclag:sonic-mclag'
        self.url_mclag_separate_ip_sonic = '/restconf/data/sonic-mclag:sonic-mclag'


        # Routing Policy / Route MAP URL
        self.url_routing_policy = '/restconf/data/openconfig-routing-policy:routing-policy'

        # L2vpn-evpn VNI mapping BGP URL
        self.url_bgp_l2vpn_evpn_vni_mapping = '/restconf/data/sonic-bgp-global:sonic-bgp-global'


        # VTEP VXLAN Configuration VNI Mapping
        self.url_vni_vlan_mapping = '/restconf/data/sonic-vxlan:sonic-vxlan'

        # Write Memory
        self.url_write_memory = '/restconf/operations/openconfig-file-mgmt-private:copy'

    def urlRequest(self, method: str, url: str, data: str = None):
        """
        :param method: Receives None, GET, DELETE, POST, PUT or PATCH
        :param url: url to be used in the API call
        :param data: json format to be sent to the call
        :return: api call response (for api_token will return the token )
        """

        try:
            if self.api_token == None:
                headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache'}
                data = {'username': "admin", 'password': "admin"}
                response = requests.request(f'{method}', url, data=json.dumps(data), headers=headers, verify=False, timeout=15)

            elif method == 'GET':
                headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache', 'Authorization': f'Bearer {self.api_token}'}
                response = requests.request("GET", url, data=data, headers=headers, verify=False, timeout=15)

            elif method == 'DELETE':
                headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache', 'Authorization': f'Bearer {self.api_token}'}
                response = requests.request("DELETE", url, data=data, headers=headers, verify=False, timeout=15)

            elif method == 'POST':
                headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache', 'Authorization': f'Bearer {self.api_token}'}
                response = requests.request("POST", url, data=data, headers=headers, verify=False, timeout=15)

            elif method == 'PUT':
                headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache', 'Authorization': f'Bearer {self.api_token}'}
                response = requests.request("PUT", url, data=data, headers=headers, verify=False, timeout=15)

            elif method == 'PATCH':
                headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache', 'Authorization': f'Bearer {self.api_token}'}
                response = requests.request("PATCH", url, data=data, headers=headers, verify=False, timeout=15)

            return response

        except:
            exit("Error URL")

    def loginRequest(self, **kwargs: dict):
        """
        Receives a Dictonary **kwargs i.e
            test_dict = {
                'username': 'admin',
                'password': 'admin',
                'address': '192.168.0.215',
                'port': '443'
            }
            Kwargs:
                kwargs['username'] (str): Sonic username
                kwargs['password'] (str): Sonic password
                kwargs['address'] (str): Sonic Switch IP address
                kwargs['port'] (str): Sonic port number

        Call the createBaseUrl() ( it will create the base URL

        get the API token calling getApiToken


        Args:
            kwargs (dict): HTTP definition type i.e GET,PUT,POST,DELETE
        """

        self.username = kwargs['username']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.port = str(kwargs['port'])
        self.createBaseUrl()
        response = self.getApiToken()
        #self.customSuccess(response=response)
        return response

    def getApiToken(self):
        """
        Login Request receives the parameters then call getApiToken to get the token to be used in this instance
        Create new API token to run the script

        Creates new API token by loging in. The new token is saved as a instance varible self.api_token.
        :return: Return API Token

        """
        login_url = self.base_url + self.url_token
        self.api_token = None
        response = self.urlRequest(url=login_url, method='POST')
        self.api_token = response.json()['access_token']
        return response

    def createBaseUrl(self):
        """
        Create the base URL to be used for other requests APIs i.e self.base_url + self.sonic_interfaces
            https://192.168.0.215:443

        Update self.base_url with the base URL
        """

        self.base_url = 'https://' + self.address + ':' + self.port

    """
    # System configuration
    """
    def hostnameConfigure(self, hostname):
        """

        :param hostname: receives hostname, send to Interfaces.hostnameSet and configures using urlRequest
        :return: return the API response
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring hostname - Hostname: {hostname}')
        url = f'{self.base_url}{self.url_system}'

        sonic_obj = SystemSonic()
        data = sonic_obj.hostnameSet(hostname=hostname)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def interfaceNamingModeConfigure(self, mode):
        """

        :param mode: receives interface naming mode, send to Interfaces.interfaceNamingSet and configures using urlRequest
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Naming Standard - MODE: {mode}')
        url = f'{self.base_url}{self.url_system}'

        sonic_obj = SystemSonic()
        data = sonic_obj.interfaceNamingSet(mode=mode)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def portGroupConfigure(self, id, speed):
        """

        :param id: i.e 1,2,3,4
        :param speed: openconfig-if-ethernet:SPEED_25GB, openconfig-if-ethernet:SPEED_10GB
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Port Group - PortGroup: {id}, SPEED: {speed}')
        url = f'{self.base_url}{self.url_portgroup}'

        sonic_obj = SystemSonic()
        data = sonic_obj.portGroupSet(id=id, speed=speed)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def anyCastMacConfigure(self, anycast_mac, ipv4_enable, ipv6_enable, vrf_name):
        """

        :param anycast_mac: i.e: 00:00:00:00:01:02
        :param ipv4_enable: i.e: true
        :param ipv6_enable: i.e: true
        :param vrf_name: i.e: default
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Anycast MAC - MAC: {anycast_mac}, VRF: {vrf_name}')
        url = f'{self.base_url}{self.url_network_instances}/network-instance={vrf_name}/openconfig-network-instance-ext:global-sag'

        sonic_obj = SystemSonic()
        data = sonic_obj.anyCastMacSet(anycast_mac=anycast_mac, ipv4_enable=ipv4_enable, ipv6_enable=ipv6_enable)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # Vlan Interface Configuration
    """
    def vlanBasicConfigure(self, name, mtu, enabled, description=None):
        """

        :param name: vlan name i.e Vlan250, Vlan150 ( upercase  "V" )
        :param mtu: 9000, 9050 etc
        :param enabled: true or false ( no shut / shut )
        :param description:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Vlan Interface - Vlan {name}')
        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vlanBasicSet(name=name, mtu=mtu, enabled=enabled, description=description)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def arpSuppressConfigure(self, vlan):
        """

        :param vlan: vlan name to enable arp suppress
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Arp Suppress - Vlan {vlan}')

        url = self.base_url + self.url_arp_suppress

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vlanArpSuppressSet(vlan=vlan)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def interfaceAnyCastGwConfigure(self, vlan, ip_address):
        """

        :param vlan:
        :param ip_address:
        :return:
        """

        print("-" * 50)
        print(f'- {self.address}: Configuring Anycast Gateway - Vlan: {vlan}, IP Address: {ip_address}')
        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.interfaceAnyCastGwSet(vlan=vlan, ip_address=ip_address)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vlanIpv4AddressConfigure(self, name, ip, prefix):
        """

        :return: Check interfaceIpv4Set for documentation
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Vlan IP Address - Vlan: {name}, IP: {ip}, Prefix: {prefix}')

        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vlanIpv4AddressSet(name=name, ip=ip, prefix=prefix)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vlanAccessConfigure(self, name, mtu, enabled, access_vlan):
        """

        :param name:
        :param mtu:
        :param enabled:
        :param access_vlan:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Access Vlan - Vlan {name}, Access: {access_vlan}')
        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vlanAccessSet(name=name, mtu=mtu, enabled=enabled, access_vlan=access_vlan)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # Interface Configuration
    """

    def physicalIntBasicConfigure(self, name, mtu, enabled, description=None):
        """

        :param name: Eth1/12, Ethernet1/12
        :param mtu: 9000, 9050 etc
        :param enabled: true or false ( no shut / shut )
        :param description:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Basic Physical Interface - Interface {name}, MTU: {mtu}, Description: {description}')

        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.physicalIntBasicSet(name=name, mtu=mtu, enabled=enabled, description=description)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response


    """
    # Loopback inteface configuration
    """

    def loopBackBasicConfigure(self, name, enabled, description=None):
        """

        :return: Check loopBackBasicSet for documentation
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Loopback Basic Interface - Interface {name}, Description: {description}')

        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.loopBackBasicSet(name=name, enabled=enabled, description=description)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response


    """
    # Ipv4 Address Configuration
    """

    def ipv4InterfaceAddressConfigure(self, name, ip, prefix):
        """

        :return: Check interfaceIpv4Set for documentation
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Interface IPv4 Address - Interface {name}, IP: {ip}, Prefix: {prefix}')

        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.interfaceIpv4Set(name=name, ip=ip, prefix=prefix)
        response = self.urlRequest(url=url, method='PATCH', data=data)
        return response

    def interfaceIpv4FullConfigure(self, name, ip, prefix, enabled, description=None):
        """

        :param name:
        :param ip:
        :param prefix:
        :param enabled:
        :param description:
        :return:
        """

        print("-" * 50)
        print(f'- {self.address}: Configuring Interface IPv4 Interface - Interface {name}, IP: {ip}, Prefix: {prefix}, Description: {description}')

        url = self.base_url + self.url_interface_all

        sonic_obj = InterfacesSonic()
        data = sonic_obj.interfaceIpv4FullSet(name=name, ip=ip, prefix=prefix, enabled=enabled, description=description)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # VTEP Vxlan Configuration
    """

    def vTepVxLanInterfaceConfigure(self, vtep_name: str, source_ip: str):
        """

        :param vtep_name:
        :param source_ip:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring VTEP Interface - Interface: {vtep_name}, Source IP: {source_ip}')

        url = self.base_url + self.url_vni_vlan_mapping

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vTepVxLanInterfaceSet(vtep_name=vtep_name, source_ip=source_ip)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vTepVxLanVniMapConfigure(self, vtep_name: str, vni_number, vlan_name: str):
        """

        :param vtep_name:
        :param vni_number:
        :param vlan_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring VTEP VNI VLAN Mapping - VTEP: {vtep_name}, VNI: {vni_number}, VLAN: {vlan_name}')


        url = self.base_url + self.url_vni_vlan_mapping

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vTepVxLanVniMapSet(vtep_name=vtep_name, vni_number=vni_number, vlan_name=vlan_name)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # PortChannel Interface Configuration
    """

    def portChannelAccessConfigure(self, name, mtu, access_vlan, admin_status):
        """

        :param name:
        :param mtu:
        :param access_vlan:
        :param admin_status:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring PortChannel Access Interface - Interface: {name}, VLAN: {access_vlan}')

        url = self.base_url + self.url_portchannel_int

        sonic_obj = InterfacesSonic()
        data = sonic_obj.portChannelAccessSet(name=name, mtu=mtu, access_vlan=access_vlan, admin_status=admin_status)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def portChannelTaggedConfigure(self, name, mtu, tagged_list_vlan, admin_status):
        """

        :param name:
        :param mtu:
        :param tagged_list_vlan:
        :param admin_status:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring PortChannel Tagged Interface - Interface: {name}, VLAN: {tagged_list_vlan}')

        url = self.base_url + self.url_portchannel_int

        sonic_obj = InterfacesSonic()
        data = sonic_obj.portChannelTaggedSet(name=name, mtu=mtu, tagged_list_vlan=tagged_list_vlan,
                                              admin_status=admin_status)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def portChannelMemberConfigure(self, int_name, port_channel_name):
        """

        :param int_name:
        :param port_channel_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring PortChannel Interface Member - Interface: {int_name}, PortChannel: {port_channel_name}')

        url = self.base_url + self.url_portchannel_int

        sonic_obj = InterfacesSonic()
        data = sonic_obj.portChannelMemberSet(int_name=int_name, port_channel_name=port_channel_name)
        response = self.urlRequest(url=url, method='PATCH', data=data)
        return response

    """
    # MCLAG Configuration
    """

    def mcLagConfigure(self, domain_id, source_ip: str, peer_ip: str, peer_link: str):
        """

        :param domain_id:
        :param source_ip:
        :param peer_ip:
        :param peer_link:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring MCLag Domain - Domain: {domain_id}, Source IP: {source_ip}, Peer IP: {peer_ip}, Peer Link: {peer_link}')

        url = self.base_url + self.url_mclag_sonic

        sonic_obj = InterfacesSonic()
        data = sonic_obj.mcLagSet(domain_id=domain_id, source_ip=source_ip, peer_ip=peer_ip, peer_link=peer_link)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def mcLagPortChannelConfigure(self, channel_group, portchannel_interface):
        """
        # it's used to configure the mclag 1, 2 to a customer interfaces to be part of the lag
        :param domain_id:
        :param source_ip:
        :param peer_ip:
        :param peer_link:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring MCLag Domain to PortChannel- MCLAG: {channel_group}, PortChannel: {portchannel_interface}')

        url = self.base_url + self.url_mclag_sonic

        sonic_obj = InterfacesSonic()
        data = sonic_obj.mcLagPortChannelSet(channel_group=channel_group, portchannel_interface=portchannel_interface)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def mcLagSeparateIpConfigure(self, name):
        """

        :param name:
        :return:
        """

        print("-" * 50)
        print(f'- {self.address}: Configuring MCLAG Separate IP - Interface: {name}')

        url = self.base_url + self.url_mclag_separate_ip_sonic

        sonic_obj = InterfacesSonic()
        data = sonic_obj.mcLagSeparateIpSet(name=name)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # VRF Configuration
    """

    def vrfConfigure(self, vrf_name):
        """

        :param vrf_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Creating VRF Instance - VRF Name: {vrf_name}')

        url = self.base_url + self.url_vrf_sonic

        sonic_obj = VrfSonic()
        data = sonic_obj.vrfSet(vrf_name=vrf_name)
        response = self.urlRequest(url=url, method='PATCH', data=data)
        return response

    def vrfInterfaceAttachConfigure(self, name, vrf_name):
        """

        :param name:
        :param vrf_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Attaching Interface to VRF Instance - VRF Name: {vrf_name}, Interface: {name}')

        url = self.base_url + self.url_network_instances + f'/network-instance={vrf_name}/interfaces'

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vrfInterfaceAttachSet(name=name)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vrfInterfaceLoopBackAttachConfigure(self, name, vrf_name):
        """

        :param name:
        :param vrf_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Attaching Loopback Interface to VRF Instance - VRF Name: {vrf_name}, Interface: {name}')

        url = self.base_url + self.url_network_instances + f'/network-instance={vrf_name}/interfaces'

        sonic_obj = InterfacesSonic()
        data = sonic_obj.vrfInterfaceLoopBackAttachSet(name=name)
        response = self.urlRequest(url=url, method='PATCH', data=data)
        return response


    def vrfVniMapConfigure(self, vrf_name, vni_number):
        """

        :param vrf_name:
        :param vni_number:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Creating VRF VNI MAP - VRF Name: {vrf_name}, VNI Number: {vni_number}')

        url = self.base_url + self.url_vrf_sonic

        sonic_obj = VrfSonic()
        data = sonic_obj.vrfVniMapSet(vrf_name=vrf_name, vni_number=vni_number)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vrfBgpGlobalConfigure(self, as_number, router_id, rd_number, rt_export, rt_import, vrf_name):
        """

        :param as_number:
        :param router_id:
        :param rd_number:
        :param rt_export:
        :param rt_import:
        :param vrf_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring VRF BGP Global Config - VRF Name: {vrf_name}, AS: {as_number}, '
              f'Router ID: {router_id}, RD: {rd_number}, RT-Import: {rt_import}, RT-Export: {rt_export}')

        url = self.base_url + self.url_network_instances + f'/network-instance={vrf_name}/protocols/protocol=BGP,bgp/'

        sonic_obj = VrfSonic()
        data = sonic_obj.vrfBgpGlobalSet(as_number=as_number, router_id=router_id, rd_number=rd_number,
                                         rt_export=rt_export, rt_import=rt_import)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vrfBgpPeerGroupL3rtrConfigure(self, pg_name, vrf_name):
        """

        :param pg_name:
        :param vrf_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Creating VRF BGP Peer Group - VRF Name: {vrf_name}, Peer Group: {pg_name}')

        url = self.base_url + self.url_network_instances + f'/network-instance={vrf_name}/protocols/protocol=BGP,bgp/'

        sonic_obj = VrfSonic()
        data = sonic_obj.vrfBgpPeerGroupL3rtrSet(pg_name=pg_name)

        response = self.urlRequest(url=url, method='PATCH', data=data)
        return response

    def vrfBgpPeerGroupMcLagPeerConfigure(self, pg_name, vrf_name):

        print("-" * 50)
        print(f'- {self.address}: Creating VRF BGP Peer Group - VRF Name: {vrf_name}, Peer Group: {pg_name}')

        url = self.base_url + self.url_network_instances + f'/network-instance={vrf_name}/protocols/protocol=BGP,bgp/'

        sonic_obj = VrfSonic()
        data = sonic_obj.vrfBgpPeerGroupMcLagPeerSet(pg_name=pg_name)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def vrfRedistributeConnectedIpv4DefaultConfigure(self, instance_name):

        print("-" * 50)
        print(f'- {self.address}: VRF IPv4 Redistribute Connected IPv4 - VRF Name: {instance_name}')

        url = self.base_url + self.url_network_instances + f'/network-instance={instance_name}/table-connections'

        sonic_obj = VrfSonic()
        data = sonic_obj.vrfRedistributeConnectedIpv4DefaultSet()
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # Routing Policy / Route MAP Configuration
    """

    def rpPrependMcLagPeerConfigure(self, name, policy_result, as_number, sequence_number, match_set: str = "ANY"):

        """

        :param name:
        :param policy_result:
        :param as_number:
        :param sequence_number:
        :param match_set:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: Configuring Route MAP - Route MAP: {name}')

        url = self.base_url + self.url_routing_policy

        sonic_obj = RoutingPolicySonic()
        data = sonic_obj.rpPrependMcLagPeerSet(name=name, policy_result=policy_result, as_number=as_number,
                                               sequence_number=sequence_number, match_set=match_set)
        response = self.urlRequest(url=url, method='PATCH', data=data)
        return response

    def redistributeConnectedIpv4DefaultConfigure(self, instance_name):

        print("-" * 50)
        print(f'- {self.address}: BGP IPv4 Redistribute Connected IPv4 - VRF Name: {instance_name}')

        url = self.base_url + self.url_network_instances + f'/network-instance={instance_name}/table-connections/'

        sonic_obj = RoutingPolicySonic()
        data = sonic_obj.redistributeConnectedIpv4DefaultSet()
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    """
    # BGP Configuration Global
    """

    def bgpGlobalConfigure(self, as_number, router_id, maximum_paths):

        """

        :param as_number:
        :param router_id:
        :param maximum_paths:
        :return:
        """

        print("-" * 50)
        print(f'- {self.address}: Configuring BGP Global Config - AS Number: {as_number}, Router ID: {router_id}')

        url = self.base_url + self.url_network_instances_bgp

        sonic_obj = BGPSonic()
        data = sonic_obj.bgpGlobalSet(as_number=as_number, router_id=router_id, maximum_paths=maximum_paths)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def bgpL2vpnVniMappingConfigure(self, vrf_name, vni_number, rd_number, rt_export, rt_import):

        """

        :param vrf_name:
        :param vni_number:
        :param rd_number:
        :param rt_export:
        :param rt_import:
        :return:
        """

        print("-" * 50)
        print(f'- {self.address}: BGP L2VPN VNI Config - VRF Name: {vrf_name}, VNI: {vni_number}, RD: {rd_number}, RT-Import: {rt_import}, RT Export: {rt_export}')

        url = self.base_url + self.url_bgp_l2vpn_evpn_vni_mapping

        sonic_obj = BGPSonic()
        data = sonic_obj.bgpL2vpnVniMappingSet(vrf_name=vrf_name, vni_number=vni_number, rd_number=rd_number,
                                               rt_export=rt_export, rt_import=rt_import)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def bgpPeerGroupUnderlayConfigure(self, pg_name):

        """

        :param pg_name:
        :return:
        """
        print("-" * 50)
        print(f'- {self.address}: BGP Peer Group - Peer Group: {pg_name}')

        url = self.base_url + self.url_network_instances_bgp

        sonic_obj = BGPSonic()
        data = sonic_obj.bgpPeerGroupUnderlaySet(pg_name=pg_name)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def bgpPeerGroupOverlayConfigure(self, pg_name, source_ip):

        print("-" * 50)
        print(f'- {self.address}: BGP Peer Group - Peer Group: {pg_name}')

        url = self.base_url + self.url_network_instances_bgp

        sonic_obj = BGPSonic()
        data = sonic_obj.bgpPeerGroupOverlaySet(pg_name=pg_name, source_ip=source_ip)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def bgpPeerGroupMcLagConfigure(self, pg_name, export_policy):

        print("-" * 50)
        print(f'- {self.address}: BGP Peer Group - Peer Group: {pg_name}, Export Policy: {export_policy}')

        url = self.base_url + self.url_network_instances_bgp

        sonic_obj = BGPSonic()
        data = sonic_obj.bgpPeerGroupMcLagSet(pg_name=pg_name, export_policy=export_policy)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def bgpNeighborConfigure(self, neighbor_address: str, peer_as, peer_group: str, description: str = None):

        print("-" * 50)
        print(f'- {self.address}: BGP Neighbor Config - Neighbor: {neighbor_address}, Peer AS: {peer_as}, Peer Group: {peer_group}, Description: {description}')

        url = self.base_url + self.url_network_instances_bgp

        sonic_obj = BGPSonic()
        data = sonic_obj.bgpNeighborSet(neighbor_address=neighbor_address, peer_as=peer_as, peer_group=peer_group,
                                        description=description)
        response = self.urlRequest(url=url, method='PATCH', data=data)

        return response

    def writeMemorySonic(self):

        print("-" * 50)
        print(f'- {self.address}: Saving Config - Write Memory')

        url = self.base_url + self.url_write_memory

        data = f'''
        {{
            "openconfig-file-mgmt-private:input": {{
                "source": "running-configuration",
                "overwrite": true,
                "destination": "startup-configuration"
            }}
        }}
        '''
        response = self.urlRequest(url=url, method='POST', data=data)

        return response


