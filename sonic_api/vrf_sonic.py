"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""


class VrfSonic():

    @staticmethod
    def vrfSet(vrf_name: str):

        """

        :param vrf_name: i.e Vrf-test-1 ( upper case "V" - it needs to start with Vrf-
        :return:
        """

        data = f'''{{
            "sonic-vrf:sonic-vrf": {{
                "VRF": {{
                    "VRF_LIST": [
                        {{
                            "fallback": false,
                            "vrf_name": "{vrf_name}"
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def vrfVniMapSet(vrf_name: str, vni_number):

        """

        :param vrf_name: i.e Vrf-test-1 ( upper case "V" - it needs to start with Vrf-
        :param vni_number: 10010
        :return:
        """

        data = f'''{{
            "sonic-vrf:sonic-vrf": {{
                "VRF": {{
                    "VRF_LIST": [
                        {{
                            "fallback": false,
                            "vni": {vni_number},
                            "vrf_name": "{vrf_name}"
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def vrfRedistributeConnectedIpv4DefaultSet():

        data = f'''
        {{
            "openconfig-network-instance:table-connections": {{
                "table-connection": [
                    {{
                        "address-family": "openconfig-types:IPV4",
                        "config": {{
                            "address-family": "openconfig-types:IPV4",
                            "dst-protocol": "openconfig-policy-types:BGP",
                            "src-protocol": "openconfig-policy-types:DIRECTLY_CONNECTED"
                        }},
                        "dst-protocol": "openconfig-policy-types:BGP",
                        "src-protocol": "openconfig-policy-types:DIRECTLY_CONNECTED"
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def vrfBgpGlobalSet(as_number, router_id: str, rd_number: str, rt_export: str, rt_import: str):
        data = f'''
        {{
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
                                                    "maximum-paths": 2
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
                                                "export-rts": [
                                                    "{rt_export}"
                                                ],
                                                "import-rts": [
                                                    "{rt_import}"
                                                ],
                                                "route-distinguisher": "{rd_number}"
                                            }},
                                            "openconfig-bgp-evpn-ext:route-advertise": {{
                                                "route-advertise-list": [
                                                    {{
                                                        "advertise-afi-safi": "openconfig-bgp-types:IPV4_UNICAST",
                                                        "config": {{
                                                            "advertise-afi-safi": "openconfig-bgp-types:IPV4_UNICAST"
                                                        }}
                                                    }}
                                                ]
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
                                        "allow-multiple-as": false
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
    def vrfBgpPeerGroupMcLagPeerSet(pg_name: str):

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
                                                    "enabled": false,
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
                                        "capability-extended-nexthop": true,
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
                                            "minimum-advertisement-interval": 0
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
    def vrfBgpPeerGroupExtRouterSet(pg_name: str):

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
                                            "enabled": false
                                        }}
                                    }},
                                    "peer-group-name": "{pg_name}",
                                    "timers": {{
                                        "config": {{
                                            "connect-retry": 5,
                                            "minimum-advertisement-interval": 0
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







