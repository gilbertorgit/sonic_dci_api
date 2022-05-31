"""
---------------------------------
 Author: Gilberto Rampini
 Date: 06/2022
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
