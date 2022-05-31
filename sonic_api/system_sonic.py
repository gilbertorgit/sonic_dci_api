"""
---------------------------------
 Author: Gilberto Rampini
 Date: 06/2022
---------------------------------
"""


class SystemSonic():

    @staticmethod
    def hostnameSet(hostname: str):

        """

        :param self:
        :param hostname: receives the hostname str
        :return: return data to be load in the API Call request
        """

        data = f'''
        {{
            "openconfig-system:system": {{
                "config": {{
                    "hostname": "{hostname}"
                }}
            }}
        }}
        '''
        return data

    @staticmethod
    def interfaceNamingSet(mode: str):
        """

        :param self:
        :param mode: Interface Naming Convention i.e -> STANDARD or NATIVE
        :return: return data to be load in the API Call request
        """
        data = f'''
                {{
                    "openconfig-system:system": {{
                        "config": {{
                            "openconfig-system-deviation:intf-naming-mode": "{mode}"
                        }}
                    }}
                }}
                '''
        return data

    @staticmethod
    def portGroupSet(id: str, speed: str="SPEED_10GB"):

        """

        :param self:
        :param id: port grou ID 1,2,3,4...
        :param speed: openconfig-if-ethernet:SPEED_25GB, openconfig-if-ethernet:SPEED_10GB
        :return: return data to be load in the API Call request
        """
        data = f'''{{
            "openconfig-port-group:port-groups": {{
                "port-group": [
                    {{
                        "config": {{
                            "speed": "openconfig-if-ethernet:{speed}"
                        }},
                        "id": "{id}"
                    }}
                ]
            }}
        }}
        '''

        return data

    @staticmethod
    def anyCastMacSet(anycast_mac: str, ipv4_enable: str, ipv6_enable: str):
        data = f'''{{
            "openconfig-network-instance-ext:global-sag": {{
                "config": {{
                    "anycast-mac": "{anycast_mac}",
                    "ipv4-enable": {ipv4_enable},
                    "ipv6-enable": {ipv6_enable}
                }}
            }}
        }}
        '''

        return data
