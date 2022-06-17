"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""

import subprocess
from re import search
from time import sleep
import time


class BasicInfra():

    def __init__(self, source_sonic_image=None, source_linux_image=None, source_apstra_image=None ):
        self.interface_list = []
        self.vrdc_list = []
        self.source_sonic_image = source_sonic_image
        self.source_linux_image = source_linux_image
        self.source_apstra_image = source_apstra_image
        self.ent_sonic_image = '/var/lib/libvirt/images/Enterprise_SONiC_OS_4.0.1.img'
        self.generic_centos_image = '/var/lib/libvirt/images/CentOS-7-x86_64-GenericCloud.qcow2'
        self.apstra_image = '/var/lib/libvirt/images/aos_server_4.0.0-314.qcow2'
        self.image_path = '/var/lib/libvirt/images/'

    @staticmethod
    def cleanMemory():

        """
        Clean linux memory
        """

        print("-" * 120)
        print("-" * 50, "Clean Memory")

        check_memory = 'free -g'
        free_memory = 'sync; echo 3 > /proc/sys/vm/drop_caches'
        subprocess.call(check_memory, shell=True)
        sleep(2)
        subprocess.call(free_memory, shell=True)
        subprocess.call(check_memory, shell=True)
        sleep(5)

    def defineLogicalInterfaces(self, name="L-", int_start=1, int_stop=40):

        """
        Define virtual logical interfaces range to connect the virtual devices
        based on the int_start and int_stop(-1) 1,40 = 1-39
        :return: returns the list of interface to be create by the createLogialInterfaces
        """
        print("-" * 120)
        print("-" * 50, "Generate Bridges")

        self.interface_list = [name + str(fabric_interface) for fabric_interface in range(int_start, int_stop)]

    def createLogicalInterfaces(self, bridge_echo=16384):

        """
        :param bridge_echo: is used to set the bitmask for logical bridges interfaces and enable the LLDP, LACP traffic
        bridge_echo = 16384 - for non compile kernel
        bridge_echo = 65535 - for compile kernel
        the if not search avoid to setup the bitmask in the Dummy interfaces ( Dummy interfaces are used to populate
        the virtual machine logical interfaces that is not used ( see any createVirtualXxxxx ( sonic, srx, vmx etc )
        :return:
        """

        print("-" * 120)
        print("-" * 50, "Create Logical Interfaces")

        for br_interface in self.interface_list:

            cmd_brctl = f'/sbin/ip link add name {br_interface} type bridge'
            cmd_ifconfig = f'/sbin/ip link set {br_interface} up'
            subprocess.call(cmd_brctl, shell=True)
            subprocess.call(cmd_ifconfig, shell=True)

            if not search("Dummy", br_interface):
                lacp_ldp = f'echo {bridge_echo} > /sys/class/net/{br_interface}/bridge/group_fwd_mask'
                subprocess.call(lacp_ldp, shell=True)

            print(f'- Creating Interface {br_interface}')

    @staticmethod
    def deleteInterface(name="L-"):

        """
        :param name: is used to search the logical interface in the linux kvm server to be deleted
        The if interfaces is to avoid to run the command if the list is empty
        <= 1 because the Popen command return '' even if no logical interface has been found which makes the list with
        lengh equal to 1 - that means empty list in this case
        :return:
        """

        print("-" * 120)
        print("-" * 50, "Deleting Logical Interfaces")

        cmd_int_list = f"/sbin/ip a | grep {name} | awk '{{print $2}}'"

        int_list = []
        int_info = subprocess.Popen(cmd_int_list, shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8').replace(':', '')
        int_list.extend(int_info.split("\n"))

        if len(int_list) <= 1:
            print("Interface list is empty")
        else:
            for br_interface in int_list:
                cmd_ifconfig = f'/sbin/ip link set {br_interface} down'
                cmd_brctl = f'/sbin/ip link delete {br_interface} type bridge'

                subprocess.call(cmd_ifconfig, shell=True)
                subprocess.call(cmd_brctl, shell=True)

                print(f'- Deleting Interface {br_interface}')

    def getVirtualMachineStatus(self, virsh_status="running", *args):

        """
        create a list with all destroyed or running virtual machine
        virsh_status: destroyed or running
        *args: list of virtual machines to be found
        :return the list of virtual machines that needs to be started or destroyed vrdc_list
        """

        for vm in args:

            cmd_virsh_list = ''
            if virsh_status == "destroyed":
                cmd_virsh_list = f"virsh list --all | egrep {vm} | awk '{{print $2}}'"
            if virsh_status == "running":
                cmd_virsh_list = f"virsh list | egrep {vm} | awk '{{print $2}}'"

            # get the output of the cmd_virsh_list, strip and decode in utf-8 - necessary to clean the list output
            vrdc_info = subprocess.Popen(cmd_virsh_list, shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')
            # creates list of the vrdc_info and clean the empty spaces
            self.vrdc_list.extend(vrdc_info.split("\n"))

    def startStopVirtualMachine(self, virsh_action):

        """
        :param virsh_action: start or destroy
        :param virsh_status: running or destroyed
        :param vm_description: i.e Virtual Sonic, Linux VM, Apstra, etc
        :param args: List of virtual machines, i.e: virsh_list_filter = ["dc1-sonic-", "dc2-sonic-", "c1_v", "c2_v"]
        :subprocess.call: run the virsh command with the action + vm
        """
        print("-" * 120)
        print("-" * 50, f"{virsh_action} - Virtual Machines")

        server_list = self.vrdc_list

        for server in server_list:
            if server != '':
                command = f'/usr/bin/virsh {virsh_action} {server}'
                subprocess.call(command, shell=True)
                sleep(1)

    def createVirtualVmDic(self, csv_file):

        """
        :param csv_file: receive the csv_file to be translated to a dictionary
        hosts = dict() - creates a empty dict
        split the csv by "," -> ['X', 'Y', 'N...']
        hosts.update({words[0]: dict()}) -> creates update hosts sending the first index and a empty dict ( nested dict )
        n = len(words) -> get the length of the list ( words )
        for i in range(1, n - 1, 2): -> creates the range from index 1 to index n - 1 and increment by 2 that means:
            for each line in the CSV file it's gonna create a nested dictionary with the key
            { words[0]: { 'i(1)': 'i+1(1+1=2)', 'i(3)': 'i+1(3+1=4)', etc... }
        :return: nested hosts dictonary
            {'dc1-sonic-leaf-1': {'hostname': 'dc1-sonic-leaf-1', 'mgmt_ip': '192.168.122.217', 'mgmt_int': 'virbr0'},
            'dc1-sonic-leaf-2': {'hostname': 'dc1-sonic-leaf-2', 'mgmt_ip': '192.168.122.218', 'mgmt_int': 'virbr0'}}
        """
        file_handle = open(csv_file)
        hosts_info_dict = dict()
        for line in file_handle:
            words = line.split(',')
            hosts_info_dict.update({words[0]: dict()})
            n = len(words)
            for i in range(1, n - 1, 2):
                if words[0] in hosts_info_dict.keys():
                    hosts_info_dict[words[0]].update({words[i]: words[i + 1]})
        return hosts_info_dict

    def getVirtualVmHostname(self, csv_file):

        """
        Get the hostname of the virtual VMs only
        :param csv_file:
        :return:
        """
        virtual_hosts = self.createVirtualVmDic(csv_file)
        return [virtual_hosts[i].get('hostname') for i in virtual_hosts.keys()]

    def createVirtualSonic(self, csv_file):

        """
        :param csv_file:
        :return:
        """
        print("-" * 120)
        print("-" * 50, "Creating Datacenter Topology")

        copy_vrdc_img = f'cp {self.source_sonic_image} {self.ent_sonic_image}'
        subprocess.call(copy_vrdc_img, shell=True)

        virtual_hosts = self.createVirtualVmDic(csv_file)

        for i in virtual_hosts.keys():
            hostname = virtual_hosts[i].get('hostname')
            mgmt_int = virtual_hosts[i].get('mgmt_int')
            mgmt_ip = virtual_hosts[i].get('mgmt_ip')
            dummy_int = virtual_hosts[i].get('dummy_int')
            xe_1 = virtual_hosts[i].get('xe_1')
            xe_2 = virtual_hosts[i].get('xe_2')
            xe_3 = virtual_hosts[i].get('xe_3')
            xe_4 = virtual_hosts[i].get('xe_4')
            xe_5 = virtual_hosts[i].get('xe_5')
            xe_6 = virtual_hosts[i].get('xe_6')
            xe_7 = virtual_hosts[i].get('xe_7')
            xe_8 = virtual_hosts[i].get('xe_8')
            xe_9 = virtual_hosts[i].get('xe_9')
            xe_10 = virtual_hosts[i].get('xe_10')
            xe_11 = virtual_hosts[i].get('xe_11')
            xe_12 = virtual_hosts[i].get('xe_12')

            print("-" * 30, f'Creating Ent Virtual Sonic {i}')

            vrdc_vm = f'cp {self.ent_sonic_image} {self.image_path}{hostname}.img'
            subprocess.call(vrdc_vm, shell=True)

            install_vrdc = f'virt-install --name {hostname} \
            --memory 4096 \
            --vcpus=2 \
            --import \
            --os-variant generic \
            --nographics \
            --noautoconsole \
            --disk path={self.image_path}{hostname}.img,size=18,device=disk,bus=ide,format=qcow2 \
            --accelerate \
            --network bridge={mgmt_int},model=e1000 \
            --network bridge={dummy_int},model=e1000 \
            --network bridge={xe_1},model=e1000 \
            --network bridge={xe_2},model=e1000 \
            --network bridge={xe_3},model=e1000 \
            --network bridge={xe_4},model=e1000 \
            --network bridge={xe_5},model=e1000 \
            --network bridge={xe_6},model=e1000 \
            --network bridge={xe_7},model=e1000 \
            --network bridge={xe_8},model=e1000 \
            --network bridge={xe_9},model=e1000 \
            --network bridge={xe_10},model=e1000 \
            --network bridge={xe_11},model=e1000 \
            --network bridge={xe_12},model=e1000'

            subprocess.call(install_vrdc, bufsize=2000, shell=True)

    def createVirtualVms(self, csv_file):

        print("-" * 120)
        print("-" * 50, "Creating Hosts VMs")

        copy_cloud_image = f'cp {self.source_linux_image} {self.image_path}'
        subprocess.call(copy_cloud_image, shell=True)

        virtual_hosts = self.createVirtualVmDic(csv_file)

        for i in virtual_hosts.keys():
            hostname = virtual_hosts[i].get('hostname')
            bond = virtual_hosts[i].get('bond')
            eth0 = virtual_hosts[i].get('eth0')
            eth1 = virtual_hosts[i].get('eth1')
            eth2 = virtual_hosts[i].get('eth2')

            print("-" * 30, f'Creating VM {i}')

            create_img = f'qemu-img create -f qcow2 -o preallocation=metadata {self.image_path}{hostname}.qcow2 15G'
            exapand_img = f'virt-resize --expand /dev/sda1 {self.generic_centos_image} {self.image_path}{hostname}.qcow2'
            add_metadata = f'genisoimage -output {self.image_path}{hostname}-config.iso -volid cidata ' \
                           f'-joliet -r vm_config/{hostname}/user-data ' \
                           f'vm_config/{hostname}/meta-data vm_config/{hostname}/network-config'

            subprocess.call(create_img, shell=True)
            subprocess.call(exapand_img, shell=True)
            subprocess.call(add_metadata, shell=True)

            if bond == "True":
                install_c_vm = f'virt-install --import --name {hostname} \
                --ram 1024 --vcpus 1 \
                --disk {self.image_path}{hostname}.qcow2,format=qcow2,bus=virtio \
                --disk {self.image_path}{hostname}-config.iso,device=cdrom \
                --network bridge={eth0},model=e1000 \
                --network bridge={eth1},model=e1000 \
                --network bridge={eth2},model=e1000 \
                --os-type=linux --os-variant=rhel7 \
                --noautoconsole \
                --accelerate'
                subprocess.call(install_c_vm, shell=True)
            else:
                install_c_vm = f'virt-install --import --name {hostname} \
                --ram 1024 --vcpus 1 \
                --disk {self.image_path}{hostname}.qcow2,format=qcow2,bus=virtio \
                --disk {self.image_path}{hostname}-config.iso,device=cdrom \
                --network bridge={eth0},model=e1000 \
                --network bridge={eth1},model=e1000 \
                --os-type=linux --os-variant=rhel7 \
                --noautoconsole \
                --accelerate'
                subprocess.call(install_c_vm, shell=True)

    def createVirtualApstra(self, csv_file):

        print("-" * 120)
        print("-" * 50, "Creating Apstra Server")

        virtual_hosts = self.createVirtualVmDic(csv_file)

        for i in virtual_hosts.keys():
            hostname = virtual_hosts[i].get('hostname')
            eth0 = virtual_hosts[i].get('eth0')
            eth1 = virtual_hosts[i].get('eth1')

            print("-" * 30, f'Creating Apstra Server {i}')

            copy_aos_image = f'cp images/{self.apstra_image} {self.image_path}{hostname}.qcow2'
            subprocess.call(copy_aos_image, shell=True)

            install_aos = f'virt-install --name={hostname} \
            --vcpu=8 \
            --ram=32768 \
            --import \
            --disk={self.image_path}{hostname}.qcow2 \
            --os-type=linux --os-variant ubuntu16.04 \
            --network bridge={eth0},model=virtio \
            --noautoconsole \
            --accelerate'

            subprocess.call(install_aos, shell=True)

    def deleteVirtualLab(self, csv_file, image_name=None):

        ############# Preciso fazer algo para deletar as imagens corretamente, isto esta errado!!!!!!
        ############# nao vai deletar tudo, vai deixar coisa pra tras e vai dar erro de execucao
        """
        virtual_hosts = self.createVrdcDic(csv_file) -> get the csv to get the hostnames to be deleted
        for i in virtual_hosts.keys(): -> by keys, get the hostname. Hostname will always match with the virtual image
            name
        """
        print("-" * 120)
        print("-" * 50, "Deleting Virtual Topology")

        virtual_hosts = self.createVirtualVmDic(csv_file)

        for i in virtual_hosts.keys():
            hostname = virtual_hosts[i].get('hostname')

            print("-" * 30, f"Deleting Virtual Image: {hostname}")

            destroy_image = f'virsh destroy {hostname}'
            undefine_image = f'virsh undefine {hostname}'
            delete_image = f"rm -f {self.image_path}{hostname}*"

            subprocess.call(destroy_image, shell=True)
            subprocess.call(undefine_image, shell=True)
            subprocess.call(delete_image, shell=True)

    def deleteSourceImages(self):

        print("-" * 120)
        print("-" * 50, "Removing Source Images: /var/lib/libvirt/images/")

        if self.source_sonic_image:
            print("-" * 20, f"Removing {self.ent_sonic_image}")
            delete_virtual_sonic = f'rm -f {self.ent_sonic_image}'
            subprocess.call(delete_virtual_sonic, shell=True)

        if self.source_linux_image:
            print("-" * 20, f"Removing {self.generic_centos_image}")
            delete_linux_image = f'rm -f {self.generic_centos_image}'
            subprocess.call(delete_linux_image, shell=True)

        if self.source_apstra_image:
            print("-" * 20, f"Removing {self.apstra_image}")
            delete_apstra_image = f"rm -f {self.apstra_image}"
            subprocess.call(delete_apstra_image, shell=True)
