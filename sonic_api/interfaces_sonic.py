"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""


class InterfacesSonic:
    """
    # Vlan
    """

    @staticmethod
    def vlanBasicSet(name: str, mtu: str, enabled: str, description: str = None):
        """
        it can be used to configure a basic VLAN
        :param name: 2 ( just the vlan number )
        :param mtu: 9000, 9050
        :param enabled: true/false (no shut / shut )
        :param description: interface description i.e: to_áspine1_interface_eth1/1
        :return:
        """
        data = f'''
        {{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "description": "{description}",
                            "enabled": {enabled},
                            "name": "Vlan{name}",
                            "mtu": {mtu},
                            "type": "iana-if-type:l2vlan"
                        }},
                        "name": "Vlan{name}"
                    }}
                ]
            }}
        }}
        '''
        return data

    @staticmethod
    def vlanShutNoShutSet(name: str, mtu, enabled, description: str = None):
        data = f'''
        {{
            "openconfig-interfaces:interface": [
                {{
                    "config": {{
                        "description": "{description}",
                        "enabled": {enabled},
                        "mtu": {mtu},
                        "name": "Vlan{name}",
                        "type": "iana-if-type:l2vlan"
                    }},
                    "name": "Vlan{name}"
                }}
            ]
        }}
        '''
        return data

    @staticmethod
    def vlanArpSuppressSet(vlan: str):
        """
        enable  neigh-suppress
        :param vlan: 2 ( just the vlan number )
        :return:
        """
        data = f'''{{
            "sonic-vxlan:sonic-vxlan": {{
                "SUPPRESS_VLAN_NEIGH": {{
                    "SUPPRESS_VLAN_NEIGH_LIST": [
                        {{
                            "name": "Vlan{vlan}",
                            "suppress": "on"
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def vrfInterfaceAttachSet(name: str):
        """
        attach interface to a specific Vrf
        :param name:  2 ( just the vlan number )
        :return:
        """
        data = f'''{{
            "openconfig-network-instance:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "id": "Vlan{name}",
                            "interface": "Vlan{name}"
                        }},
                        "id": "Vlan{name}"
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def vrfInterfaceLoopBackAttachSet(name: str):
        """
        attach interface to a specific Vrf
        :param name:  2 ( just the vlan number )
        :return:
        """
        data = f'''{{
            "openconfig-network-instance:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "id": "{name}",
                            "interface": "{name}"
                        }},
                        "id": "{name}"
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def vlanIpv4AddressSet(name: str, ip: str, prefix):
        data = f'''
        {{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "name": "Vlan{name}",
                        "openconfig-vlan:routed-vlan": {{
                            "openconfig-if-ip:ipv4": {{
                                "addresses": {{
                                    "address": [
                                        {{
                                            "config": {{
                                                "ip": "{ip}",
                                                "prefix-length": {prefix},
                                                "secondary": false
                                            }},
                                            "ip": "{ip}"
                                        }}
                                    ]
                                }}
                            }}
                        }}
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def vlanAccessSet(name, mtu, enabled, access_vlan):

        data = f'''
        {{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "enabled": {enabled},
                            "mtu": {mtu},
                            "name": "{name}",
                            "type": "iana-if-type:ethernetCsmacd"
                        }},
                        "name": "{name}",
                        "openconfig-if-ethernet:ethernet": {{
                            "openconfig-vlan:switched-vlan": {{
                                "config": {{
                                    "access-vlan": {access_vlan},
                                    "interface-mode": "ACCESS"
                                }}
                            }}
                        }}
                    }}
                ]
            }}
        }}
        '''

        return data

    """
    # Anycast Gateway
    """

    @staticmethod
    def interfaceAnyCastGwSet(vlan: str, ip_address: str):
        """

        :param vlan: vlan name i.e 2 ( just the vlan number )
        :param ip_address: anycast gateway ip i.e 192.168.10.1/24
        :return: return  data
        """

        data = f'''{{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "name": "Vlan{vlan}",
                        "openconfig-vlan:routed-vlan": {{
                            "openconfig-if-ip:ipv4": {{
                                "openconfig-interfaces-ext:sag-ipv4": {{
                                    "config": {{
                                        "static-anycast-gateway": [
                                            "{ip_address}"
                                        ]
                                    }}
                                }}
                            }}
                        }}
                    }}
                ]
            }}
        }}
        '''

        return data

    """
    # PortChannel
    """

    @staticmethod
    def portChannelAccessSet(name: str, mtu: int, access_vlan: str, admin_status: str):
        """

        :param name: i.e PortChannel2
        :param mtu: 9050
        :param access_vlan: 10
        :param admin_status: up
        :return:
        """
        data = f'''{{
            "sonic-portchannel:sonic-portchannel": {{
                "PORTCHANNEL": {{
                    "PORTCHANNEL_LIST": [
                        {{
                            "access_vlan": "{access_vlan}",
                            "admin_status": "{admin_status}",
                            "mtu": {mtu},
                            "name": "{name}"
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def portChannelTaggedSet(name: str, mtu: int, tagged_list_vlan: list, admin_status: str):
        """

        :param name: i.e PortChannel2
        :param mtu: 9050
        :param tagged_list_vlan: need to be a list of strings [ "2-3", "10", "20", "100" ] - need to be between " "
        :param admin_status: up
        :return:
        """
        data = f'''{{
            "sonic-portchannel:sonic-portchannel": {{
                "PORTCHANNEL": {{
                    "PORTCHANNEL_LIST": [
                        {{
                            "admin_status": "{admin_status}",
                            "mtu": {mtu},
                            "name": "{name}",
                            "tagged_vlans": [{tagged_list_vlan}]
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def portChannelMemberSet(int_name: str, port_channel_name: str):
        """

        :param int_name: Eth1/6
        :param portchannel_name: PortChannel1
        :return:
        """

        data = f'''{{
            "sonic-portchannel:sonic-portchannel": {{
                "PORTCHANNEL_MEMBER": {{
                    "PORTCHANNEL_MEMBER_LIST": [
                        {{
                            "ifname": "{int_name}",
                            "name": "{port_channel_name}"
                        }}
                    ]
                }}
            }}
        }}
        '''
        return data

    """
    # MCLAG
    """

    @staticmethod
    def mcLagSet(domain_id, source_ip: str, peer_ip: str, peer_link: str):
        data = f'''
        {{
            "sonic-mclag:sonic-mclag": {{
                "MCLAG_DOMAIN": {{
                    "MCLAG_DOMAIN_LIST": [
                        {{
                            "delay_restore": 90,
                            "domain_id": {domain_id},
                            "keepalive_interval": 1,
                            "peer_ip": "{peer_ip}",
                            "peer_link": "{peer_link}",
                            "session_timeout": 30,
                            "source_ip": "{source_ip}"
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def mcLagPortChannelSet(channel_group, portchannel_interface):
        data = f'''
        {{
            "sonic-mclag:sonic-mclag": {{
                "MCLAG_INTERFACE": {{
                    "MCLAG_INTERFACE_LIST": [
                        {{
                            "domain_id": {channel_group},
                            "if_name": "{portchannel_interface}",
                            "if_type": "PortChannel"
                        }}
                    ]
                }}
            }}
        }}
        '''
        return data

    @staticmethod
    def mcLagSeparateIpSet(name: str):
        data = f'''{{
            "sonic-mclag:sonic-mclag": {{
                "MCLAG_UNIQUE_IP": {{
                    "MCLAG_UNIQUE_IP_LIST": [
                        {{
                            "if_name": "Vlan{name}",
                            "unique_ip": "enable"
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    """
    # Physical Interface
    """

    @staticmethod
    def physicalIntBasicSet(name: str, mtu: str, enabled: str, description: str = None):
        """
        it can be used to configure Interface without any additional parameters ( ip, etc )
        :param name: Vlan250, Eth1/12, Ethernet1/12
        :param mtu: 9000, 9050
        :param enabled: true/false (no shut / shut )
        :param description: interface description i.e: to_spine1_interface_eth1/1
        :return:
        """
        data = f'''
            {{
                "openconfig-interfaces:interfaces": {{
                    "interface": [
                        {{
                            "config": {{
                                "description": "{description}",
                                "enabled": {enabled},
                                "name": "{name}",
                                "mtu": {mtu},
                                "type": "iana-if-type:ethernetCsmacd"
                            }},
                            "name": "{name}"
                        }}
                    ]
                }}
            }}
            '''
        return data

    """
    # Loopback
    """

    @staticmethod
    def loopBackBasicSet(name: str, enabled, description=None):
        """

        :param name: Loopback name i.e  Loopback250
        :param enabled: true/false
        :param description:
        :return:

        To attach a VRF use vrfInterfaceAttachSet
        to attach an IPv4 use: interfaceIpv4Set
        """

        data = f'''{{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "description": "{description}",
                            "enabled": {enabled},
                            "name": "{name}",
                            "type": "iana-if-type:softwareLoopback"
                        }},
                        "name": "{name}"
                    }}
                ]
            }}
        }}
        '''

        return data

    def interfaceL2Set(self):
        pass

    """
    # IPv4 Interface configuration
    """

    @staticmethod
    def interfaceIpv4Set(name: str, ip: str, prefix):
        """

        :param name: Loopback0, Eth1/2, Vlan250
        :param ip: 10.0.0.1, 20.0.0.2
        :param prefix: 24, 32, 25
        :return:
        """

        data = f'''{{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "name": "{name}",
                        "subinterfaces": {{
                            "subinterface": [
                                {{
                                    "config": {{
                                        "index": 0
                                    }},
                                    "index": 0,
                                    "openconfig-if-ip:ipv4": {{
                                        "addresses": {{
                                            "address": [
                                                {{
                                                    "config": {{
                                                        "ip": "{ip}",
                                                        "prefix-length": {prefix},
                                                        "secondary": false
                                                    }},
                                                    "ip": "{ip}"
                                                }}
                                            ]
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def interfaceIpv4FullSet(name: str, enabled, ip: str, prefix, description: str = None):
        """
        this module is used to configure the entire interface + ipv4
        to configure just the physical interface: physicalIntBasicSet
        to configure just the ipv4 address: interfaceIpv4Set

        :param name: interface name Eth1/2, Ethernet1/2
        :param enabled: true/false ( no shut/ shut )
        :param ip: 10.0.0.1
        :param prefix: 31
        :param description: interface description
        :return:
        """
        data = f'''
        {{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "description": "{description}",
                            "enabled": {enabled},
                            "name": "{name}",
                            "type": "iana-if-type:ethernetCsmacd"
                        }},
                        "name": "{name}",
                        "subinterfaces": {{
                            "subinterface": [
                                {{
                                    "config": {{
                                        "index": 0
                                    }},
                                    "index": 0,
                                    "openconfig-if-ip:ipv4": {{
                                        "addresses": {{
                                            "address": [
                                                {{
                                                    "config": {{
                                                        "ip": "{ip}",
                                                        "prefix-length": {prefix},
                                                        "secondary": false
                                                    }},
                                                    "ip": "{ip}"
                                                }}
                                            ]
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def vTepVxLanInterfaceSet(vtep_name: str, source_ip: str):

        data = f'''
        {{
            "openconfig-interfaces:interfaces": {{
                "interface": [
                    {{
                        "config": {{
                            "name": "{vtep_name}",
                            "type": "openconfig-if-types-ext:IF_NVE"
                        }},
                        "name": "vtep1",
                        "openconfig-vxlan:vxlan-if": {{
                            "config": {{
                                "source-vtep-ip": "{source_ip}"
                            }}
                        }}
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def vTepVxLanVniMapSet(vtep_name: str, vni_number, vlan_name: str):

        data = f'''
        {{
            "sonic-vxlan:sonic-vxlan": {{
                "VXLAN_TUNNEL_MAP": {{
                    "VXLAN_TUNNEL_MAP_LIST": [
                        {{
                            "mapname": "map_{vni_number}_Vlan{vlan_name}",
                            "name": "{vtep_name}",
                            "vlan": "Vlan{vlan_name}",
                            "vni": {vni_number}
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data