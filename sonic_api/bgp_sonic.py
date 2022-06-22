"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""


class BGPSonic():

    @staticmethod
    def bgpGlobalSet(as_number, router_id, maximum_paths):

        """

        :param as_number: 65103
        :param router_id: 10.0.0.1
        :param maximum_paths: 16
        :return:
        """

        data = f'''{{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "global": {{
                            "afi-safis": {{
                                "afi-safi": [
                                    {{
                                        "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                        "config": {{
                                            "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST"
                                        }},
                                        "route-flap-damping": {{
                                            "config": {{
                                                "enabled": true
                                            }}
                                        }},
                                        "use-multiple-paths": {{
                                            "ebgp": {{
                                                "config": {{
                                                    "maximum-paths": {maximum_paths}
                                                }}
                                            }},
                                            "ibgp": {{
                                                "config": {{
                                                    "equal-cluster-length": false,
                                                    "maximum-paths": 2
                                                }}
                                            }}
                                        }}
                                    }},
                                    {{
                                        "afi-safi-name": "openconfig-bgp-types:L2VPN_EVPN",
                                        "config": {{
                                            "afi-safi-name": "openconfig-bgp-types:L2VPN_EVPN"
                                        }},
                                        "l2vpn-evpn": {{
                                            "openconfig-bgp-evpn-ext:config": {{
                                                "advertise-all-vni": true,
                                                "advertise-default-gw": false
                                            }}
                                        }}
                                    }}
                                ]
                            }},
                            "config": {{
                                "as": {as_number},
                                "ebgp-requires-policy": false,
                                "fast-external-failover": true,
                                "hold-time": 180,
                                "keepalive-interval": 60,
                                "network-import-check": true,
                                "router-id": "{router_id}"
                            }},
                            "logging-options": {{
                                "config": {{
                                    "log-neighbor-state-changes": true
                                }}
                            }},
                            "route-selection-options": {{
                                "config": {{
                                    "always-compare-med": false,
                                    "external-compare-router-id": false,
                                    "ignore-as-path-length": false
                                }}
                            }},
                            "use-multiple-paths": {{
                                "ebgp": {{
                                    "config": {{
                                        "allow-multiple-as": true,
                                        "as-set": false
                                    }}
                                }}
                            }}
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data

    @staticmethod
    def bgpL2vpnVniMappingSet(vrf_name: str, vni_number, rd_number: str, rt_export: str, rt_import: str):

        """

        :param vrf_name: default
        :param vni_number: 5200
        :param rd_number: 10.10.10.3:200
        :param rt_export: 5200:1
        :param rt_import: 5200:1
        :return:
        """

        data = f'''{{
            "sonic-bgp-global:sonic-bgp-global": {{
                "BGP_GLOBALS_EVPN_VNI": {{
                    "BGP_GLOBALS_EVPN_VNI_LIST": [
                        {{
                            "afi-safi-name": "L2VPN_EVPN",
                            "export-rts": [
                                "{rt_export}"
                            ],
                            "import-rts": [
                                "{rt_import}"
                            ],
                            "route-distinguisher": "{rd_number}",
                            "vni-number": {vni_number},
                            "vrf": "{vrf_name}"
                        }}
                    ]
                }}
            }}
        }}
        '''
        return data



    @staticmethod
    def bgpPeerGroupUnderlaySet(pg_name):
        """

        :param pg_name: fabric-underlay
        :return:
        """

        data = f'''{{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "peer-groups": {{
                            "peer-group": [
                                {{
                                    "afi-safis": {{
                                        "afi-safi": [
                                            {{
                                                "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                                "config": {{
                                                    "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                                    "enabled": true,
                                                    "route-reflector-client": false,
                                                    "send-community": "BOTH",
                                                    "soft-reconfiguration-in": true
                                                }},
                                                "ipv4-unicast": {{
                                                    "config": {{
                                                        "send-default-route": false
                                                    }},
                                                    "prefix-limit": {{
                                                        "config": {{
                                                            "prevent-teardown": false
                                                        }}
                                                    }}
                                                }}
                                            }}
                                        ]
                                    }},
                                    "config": {{
                                        "capability-extended-nexthop": false,
                                        "enabled": true,
                                        "peer-group-name": "{pg_name}"
                                    }},
                                    "ebgp-multihop": {{
                                        "config": {{
                                            "enabled": false
                                        }}
                                    }},
                                    "enable-bfd": {{
                                        "config": {{
                                            "enabled": true
                                        }}
                                    }},
                                    "peer-group-name": "{pg_name}",
                                    "timers": {{
                                        "config": {{
                                            "connect-retry": 5,
                                            "hold-time": 3,
                                            "keepalive-interval": 1,
                                            "minimum-advertisement-interval": 5
                                        }}
                                    }},
                                    "transport": {{
                                        "config": {{
                                            "passive-mode": false
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data


    @staticmethod
    def bgpPeerGroupOverlaySet(pg_name, source_ip):

        """

        :param pg_name: fabric-overlay
        :param source_ip: 10.10.10.3, usually loopback address
        :return:
        """
        data = f'''{{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "peer-groups": {{
                            "peer-group": [
                                {{
                                    "afi-safis": {{
                                        "afi-safi": [
                                            {{
                                                "afi-safi-name": "openconfig-bgp-types:L2VPN_EVPN",
                                                "config": {{
                                                    "afi-safi-name": "openconfig-bgp-types:L2VPN_EVPN",
                                                    "enabled": true
                                                }}
                                            }}
                                        ]
                                    }},
                                    "config": {{
                                        "capability-extended-nexthop": false,
                                        "enabled": true,
                                        "peer-group-name": "{pg_name}"
                                    }},
                                    "ebgp-multihop": {{
                                        "config": {{
                                            "enabled": true,
                                            "multihop-ttl": 2
                                        }}
                                    }},
                                    "peer-group-name": "{pg_name}",
                                    "timers": {{
                                        "config": {{
                                            "connect-retry": 5,
                                            "hold-time": 3,
                                            "keepalive-interval": 1,
                                            "minimum-advertisement-interval": 5
                                        }}
                                    }},
                                    "transport": {{
                                        "config": {{
                                            "local-address": "{source_ip}",
                                            "passive-mode": false
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data

    @staticmethod
    def bgpPeerGroupMcLagSet(pg_name, export_policy):

        """

        :param pg_name: mclag-peer
        :param export_policy: MlagPeer - route-map name
        :return:
        """
        data = f'''{{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "peer-groups": {{
                            "peer-group": [
                                {{
                                    "afi-safis": {{
                                        "afi-safi": [
                                            {{
                                                "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                                "apply-policy": {{
                                                    "config": {{
                                                        "export-policy": [
                                                            "{export_policy}"
                                                        ]
                                                    }}
                                                }},
                                                "config": {{
                                                    "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                                    "enabled": true,
                                                    "route-reflector-client": false,
                                                    "send-community": "BOTH",
                                                    "soft-reconfiguration-in": true
                                                }},
                                                "ipv4-unicast": {{
                                                    "config": {{
                                                        "send-default-route": false
                                                    }},
                                                    "prefix-limit": {{
                                                        "config": {{
                                                            "prevent-teardown": false
                                                        }}
                                                    }}
                                                }}
                                            }}
                                        ]
                                    }},
                                    "config": {{
                                        "capability-extended-nexthop": false,
                                        "enabled": true,
                                        "peer-group-name": "{pg_name}"
                                    }},
                                    "ebgp-multihop": {{
                                        "config": {{
                                            "enabled": false
                                        }}
                                    }},
                                    "enable-bfd": {{
                                        "config": {{
                                            "enabled": true
                                        }}
                                    }},
                                    "peer-group-name": "{pg_name}",
                                    "timers": {{
                                        "config": {{
                                            "connect-retry": 5,
                                            "hold-time": 3,
                                            "keepalive-interval": 1,
                                            "minimum-advertisement-interval": 5
                                        }}
                                    }},
                                    "transport": {{
                                        "config": {{
                                            "passive-mode": false
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data

    @staticmethod
    def bgpPeerGroupEvpnGwSet(pg_name, source_ip, multi_hop):

        data = f'''
        {{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "peer-groups": {{
                            "peer-group": [
                                {{
                                    "afi-safis": {{
                                        "afi-safi": [
                                            {{
                                                "afi-safi-name": "openconfig-bgp-types:L2VPN_EVPN",
                                                "config": {{
                                                    "afi-safi-name": "openconfig-bgp-types:L2VPN_EVPN",
                                                    "enabled": true
                                                }}
                                            }}
                                        ]
                                    }},
                                    "config": {{
                                        "enabled": true,
                                        "peer-group-name": "{pg_name}"
                                    }},
                                    "ebgp-multihop": {{
                                        "config": {{
                                            "enabled": true,
                                            "multihop-ttl": {multi_hop}
                                        }}
                                    }},
                                    "peer-group-name": "{pg_name}",
                                    "timers": {{
                                        "config": {{
                                            "connect-retry": 5,
                                            "hold-time": 30,
                                            "keepalive-interval": 10,
                                            "minimum-advertisement-interval": 5
                                        }}
                                    }},
                                    "transport": {{
                                        "config": {{
                                            "local-address": "{source_ip}",
                                            "passive-mode": false
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data

    @staticmethod
    def bgpPeerGroupExtRouterSet(pg_name, multi_hop):

        data = f'''
        {{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "peer-groups": {{
                            "peer-group": [
                                {{
                                    "afi-safis": {{
                                        "afi-safi": [
                                            {{
                                                "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                                "allow-own-as": {{
                                                    "config": {{
                                                        "as-count": 1,
                                                        "enabled": true,
                                                        "origin": false
                                                    }}
                                                }},
                                                "config": {{
                                                    "afi-safi-name": "openconfig-bgp-types:IPV4_UNICAST",
                                                    "enabled": true,
                                                    "route-reflector-client": false,
                                                    "send-community": "BOTH",
                                                    "soft-reconfiguration-in": true
                                                }},
                                                "ipv4-unicast": {{
                                                    "config": {{
                                                        "send-default-route": false
                                                    }},
                                                    "prefix-limit": {{
                                                        "config": {{
                                                            "prevent-teardown": false
                                                        }}
                                                    }}
                                                }},
                                                "next-hop-self": {{
                                                    "config": {{
                                                        "enabled": true
                                                    }}
                                                }}
                                            }}
                                        ]
                                    }},
                                    "config": {{
                                        "enabled": true,
                                        "peer-group-name": "{pg_name}"
                                    }},
                                    "ebgp-multihop": {{
                                        "config": {{
                                            "enabled": true,
                                            "multihop-ttl": {multi_hop}
                                        }}
                                    }},
                                    "peer-group-name": "{pg_name}",
                                    "timers": {{
                                        "config": {{
                                            "connect-retry": 5,
                                            "minimum-advertisement-interval": 5
                                        }}
                                    }},
                                    "transport": {{
                                        "config": {{
                                            "passive-mode": false
                                        }}
                                    }}
                                }}
                            ]
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data

    @staticmethod
    def bgpNeighborSet(neighbor_address: str, peer_as, peer_group: str, description: str = None):
        """

        :param neighbor_address: 10.0.0.0
        :param peer_as: 65101
        :param peer_group: fabric-overlay, fabric-underlay
        :param description: to_neighbor_X
        :return:
        """

        data = f'''{{
            "openconfig-network-instance:protocol": [
                {{
                    "bgp": {{
                        "neighbors": {{
                            "neighbor": [
                                {{
                                    "config": {{
                                        "description": "{description}",
                                        "neighbor-address": "{neighbor_address}",
                                        "peer-as": {peer_as},
                                        "peer-group": "{peer_group}"
                                    }},
                                    "neighbor-address": "{neighbor_address}"
                                }}
                            ]
                        }}
                    }},
                    "identifier": "openconfig-policy-types:BGP",
                    "name": "bgp"
                }}
            ]
        }}
        '''

        return data



