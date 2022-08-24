"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""


class RoutingPolicySonic:

    @staticmethod
    def rpPrependMcLagPeerSet(name: str, policy_result: str, as_number, sequence_number, match_set: str = "ANY"):
        """
        used to create route-map to prepend local AS between MCLAG BGP Peer

        :param name: route map name
        :param policy_result: i.e ACCEPT_ROUTE
        :param as_number: 65103
        :param sequence_number: 10
        :param match_set: ANY
        :return:
        """

        data = f'''{{
            "openconfig-routing-policy:routing-policy": {{
                "policy-definitions": {{
                    "policy-definition": [
                        {{
                            "config": {{
                                "name": "{name}"
                            }},
                            "name": "{name}",
                            "statements": {{
                                "statement": [
                                    {{
                                        "actions": {{
                                            "config": {{
                                                "policy-result": "{policy_result}"
                                            }},
                                            "openconfig-bgp-policy:bgp-actions": {{
                                                "set-as-path-prepend": {{
                                                    "config": {{
                                                        "openconfig-routing-policy-ext:asn-list": "{as_number},{as_number},{as_number}"
                                                    }}
                                                }}
                                            }}
                                        }},
                                        "conditions": {{
                                            "match-prefix-set": {{
                                                "config": {{
                                                    "match-set-options": "{match_set}"
                                                }}
                                            }},
                                            "openconfig-bgp-policy:bgp-conditions": {{
                                                "match-as-path-set": {{
                                                    "config": {{
                                                        "match-set-options": "{match_set}"
                                                    }}
                                                }}
                                            }}
                                        }},
                                        "config": {{
                                            "name": "{sequence_number}"
                                        }},
                                        "name": "{sequence_number}"
                                    }}
                                ]
                            }}
                        }}
                    ]
                }}
            }}
        }}
        '''

        return data

    @staticmethod
    def redistributeConnectedIpv4DefaultSet():
        data = f'''{{
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


