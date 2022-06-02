
from base_sonic import *



"""
it's an old way to create a nested dictonary - interesting to have it documented
    def getSystemTab(self, file, sheet_name):

        db = self.read_excel_data(file, sheet_name)

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
"""

if __name__ == "__main__":
    a = Sonic()
    test_dict = {
        'username': 'admin',
        'password': 'admin',
        'address': '192.168.0.218',
        'port': '443'
    }
    a.loginRequest(**test_dict)
    # a.getAllInterfaces()

    """
    """

    """
    # System Configuration basic configuration
    """
    a.hostnameConfigure("leaf-test-1")
    a.interfaceNamingModeConfigure("STANDARD")
    a.portGroupConfigure("1", "SPEED_10GB")
    a.portGroupConfigure("2", "SPEED_10GB")
    a.portGroupConfigure("3", "SPEED_10GB")
    a.portGroupConfigure("4", "SPEED_10GB")
    a.portGroupConfigure("5", "SPEED_10GB")
    a.anyCastMacConfigure("00:00:00:00:01:02", "true", "true", "default")

    """
    #Create VRF
    """
    a.vrfConfigure("Vrf-customer-1")
    a.vrfConfigure("Vrf-customer-2")

    """
    #basic vlan configuration
    """

    a.vlanBasicConfigure("Vlan2", "9050", "true", "Vrf-Customer-1-Vlan")
    a.arpSuppressConfigure("Vlan2")
    a.vrfInterfaceAttachConfigure("Vlan2", "Vrf-customer-1")

    a.vlanBasicConfigure("Vlan3", "9050", "true", "Vrf-Customer-2-Vlan")
    a.arpSuppressConfigure("Vlan3")
    a.vrfInterfaceAttachConfigure("Vlan3", "Vrf-customer-2")

    a.vlanBasicConfigure("Vlan10", "9000", "true")
    a.arpSuppressConfigure("Vlan10")
    a.vrfInterfaceAttachConfigure("Vlan10", "Vrf-customer-1")
    a.interfaceAnyCastGwConfigure("Vlan10", "192.168.10.1/24")

    a.vlanBasicConfigure("Vlan20", "9000", "true")
    a.arpSuppressConfigure("Vlan20")
    a.vrfInterfaceAttachConfigure("Vlan20", "Vrf-customer-1")
    a.interfaceAnyCastGwConfigure("Vlan20", "192.168.20.1/24")

    a.vlanBasicConfigure("Vlan100", "9000", "true")
    a.arpSuppressConfigure("Vlan100")
    a.vrfInterfaceAttachConfigure("Vlan100", "Vrf-customer-2")
    a.interfaceAnyCastGwConfigure("Vlan100", "192.168.100.1/24")

    a.vlanBasicConfigure("Vlan200", "9000", "true")
    a.arpSuppressConfigure("Vlan200")
    a.vrfInterfaceAttachConfigure("Vlan200", "Vrf-customer-2")
    a.interfaceAnyCastGwConfigure("Vlan200", "192.168.200.1/24")

    """
    # Loopback Configuration
    """
    a.loopBackBasicConfigure("Loopback0", "true", "router-id")
    a.ipv4InterfaceAddressConfigure("Loopback0", "10.10.10.3", "32")

    a.loopBackBasicConfigure("Loopback1", "true", "vtep_loopback")
    a.ipv4InterfaceAddressConfigure("Loopback1", "10.10.10.10", "32")

    a.loopBackBasicConfigure("Loopback2", "true", "vrf1_loopback")
    a.vrfInterfaceLoopBackAttachConfigure("Loopback2", "Vrf-customer-1")
    a.ipv4InterfaceAddressConfigure("Loopback2", "10.100.100.1", "32")

    a.loopBackBasicConfigure("Loopback3", "true", "vrf2_loopback")
    a.vrfInterfaceLoopBackAttachConfigure("Loopback3", "Vrf-customer-2")
    a.ipv4InterfaceAddressConfigure("Loopback3", "10.100.100.5", "32")

    """
    # PortChannel Configuration -> MClag, Vlan2999 flow
    """

    a.portChannelTaggedConfigure("PortChannel2", 9050, '"2-3", "10", "20", "100", "200", "2999"', "up")
    a.mcLagConfigure(1, "10.101.101.0", "10.101.101.1", "PortChannel2")
    a.vlanBasicConfigure("Vlan2999", "9050", "true")
    a.mcLagSeparateIpConfigure("Vlan2999")
    a.vlanIpv4AddressConfigure("Vlan2999", "10.101.101.0", "31")

    a.portChannelAccessConfigure("PortChannel1", 9000, "10", "up")

    """
    # Physical Interfaces Configuration
    """

    a.interfaceIpv4FullConfigure("Eth1/2", "10.0.0.3", "31", "true", "to_spine1")
    a.interfaceIpv4FullConfigure("Eth1/3", "10.0.0.11", "31", "true", "to_spine2")

    a.physicalIntBasicConfigure("Eth1/6", 9000, "true", "sonic-mclag-leaf-1-customer1-vlan10")
    a.physicalIntBasicConfigure("Eth1/12", 9050, "true", "to_mclag_leaf_pair")

    a.portChannelMemberConfigure("Eth1/6", "PortChannel1")
    a.portChannelMemberConfigure("Eth1/12", "PortChannel2")

    a.vlanAccessConfigure("Eth1/8", 9100, "true", 100)

    """
    # Routing Policy Configuration - Route MAP
    """

    a.rpPrependMcLagPeerConfigure("MlagPeer", "ACCEPT_ROUTE", "65103", "10", "ANY")

    """
    # BGP Configuration
    """

    a.bgpGlobalConfigure(65103, "10.10.10.3", 16)
    a.redistributeConnectedIpv4DefaultConfigure("default")

    a.bgpPeerGroupUnderlayConfigure("fabric-underlay")
    a.bgpPeerGroupOverlayConfigure("fabric-overlay", "10.10.10.3")
    a.bgpPeerGroupMcLagConfigure("mclag-peer", "MlagPeer")

    a.bgpNeighborConfigure("10.10.0.2", 65101, "fabric-underlay", "to_dc1-sonic-spine1")
    a.bgpNeighborConfigure("10.10.0.10", 65102, "fabric-underlay", "to_dc1-sonic-spine2")
    a.bgpNeighborConfigure("10.10.10.1", 65101, "fabric-overlay", "to_dc1-sonic-spine1-evpn-overlay")
    a.bgpNeighborConfigure("10.10.10.2", 65102, "fabric-overlay", "to_dc1-sonic-spine2-evpn-overlay")
    a.bgpNeighborConfigure("10.101.101.1", 65104, "mclag-peer", "facing_sonic-mclag-leaf2")

    a.bgpL2vpnVniMappingConfigure("default", 5010, "10.10.10.3:10", "5010:1", "5010:1")
    a.bgpL2vpnVniMappingConfigure("default", 5020, "10.10.10.3:20", "5020:1", "5020:1")
    a.bgpL2vpnVniMappingConfigure("default", 5100, "10.10.10.3:100", "5100:1", "5100:1")
    a.bgpL2vpnVniMappingConfigure("default", 5200, "10.10.10.3:200", "5200:1", "5200:1")

    a.vrfBgpGlobalConfigure(65103, "10.100.100.1", "10.10.10.3:2", "10010:1", "10010:1", "Vrf-customer-1")
    a.vrfRedistributeConnectedIpv4DefaultConfigure("Vrf-customer-1")
    a.vrfBgpPeerGroupL3rtrConfigure("l3rtr", "Vrf-customer-1")
    a.vrfBgpPeerGroupMcLagPeerConfigure("mclag-peer", "Vrf-customer-1")

    a.vrfBgpGlobalConfigure(65103, "10.100.100.5", "10.10.10.3:3", "10020:1", "10020:1", "Vrf-customer-2")
    a.vrfRedistributeConnectedIpv4DefaultConfigure("Vrf-customer-2")
    a.vrfBgpPeerGroupL3rtrConfigure("l3rtr", "Vrf-customer-2")
    a.vrfBgpPeerGroupMcLagPeerConfigure("mclag-peer", "Vrf-customer-2")

    """
    # VTEP Configuration - VXLAN
    """

    a.vTepVxLanInterfaceConfigure("vtep1", "10.10.10.10")
    a.vTepVxLanVniMapConfigure("vtep1", 10010, "2")
    a.vTepVxLanVniMapConfigure("vtep1", 10020, "3")
    a.vTepVxLanVniMapConfigure("vtep1", 5010, "10")
    a.vTepVxLanVniMapConfigure("vtep1", 5020, "20")
    a.vTepVxLanVniMapConfigure("vtep1", 5100, "100")
    a.vTepVxLanVniMapConfigure("vtep1", 5200, "200")
    a.vrfVniMapConfigure("Vrf-customer-1", 10010)
    a.vrfVniMapConfigure("Vrf-customer-2", 10020)
