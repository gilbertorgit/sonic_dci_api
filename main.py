"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""

from basicInfra import *
import routers_config

sonic_image = 'images/Enterprise_SONiC_OS_4.0.1.img'
linux_image = 'images/CentOS-7-x86_64-GenericCloud.qcow2'

logical_interfaces = "L-"
dummy_interfaces = "dummy-int-"


def start_topology():

    print("#" * 150)
    print("#" * 100, "Start Virtual Topology")

    virtual_vm = BasicInfra()

    virtual_vm.cleanMemory()

    virtual_vm.defineLogicalInterfaces(logical_interfaces, 1, 40)
    virtual_vm.createLogicalInterfaces(65535)

    virtual_vm.defineLogicalInterfaces(dummy_interfaces, 1, 20)
    virtual_vm.createLogicalInterfaces()

    vrdc_hostname_list = virtual_vm.getVirtualVmHostname("vrdc_info.csv")
    vm_hostname_list = virtual_vm.getVirtualVmHostname("vm_info.csv")
    virtual_vm.getVirtualMachineStatus("destroyed", *vrdc_hostname_list)
    virtual_vm.getVirtualMachineStatus("destroyed", *vm_hostname_list)
    virtual_vm.startStopVirtualMachine("start")


def stop_topology():

    print("#" * 150)
    print("#" * 100, "Stop Virtual Topology")

    virtual_vm = BasicInfra()

    vrdc_hostname_list = virtual_vm.getVirtualVmHostname("vrdc_info.csv")
    vm_hostname_list = virtual_vm.getVirtualVmHostname("vm_info.csv")
    virtual_vm.getVirtualMachineStatus("running", *vrdc_hostname_list)
    virtual_vm.getVirtualMachineStatus("running", *vm_hostname_list)
    virtual_vm.startStopVirtualMachine("destroy")

    virtual_vm.deleteInterface(logical_interfaces)
    virtual_vm.deleteInterface(dummy_interfaces)

    virtual_vm.cleanMemory()


def create_topology():

    print("#" * 150)
    print("#" * 100, "Create Virtual Topology")

    virtual_vm = BasicInfra(source_sonic_image=sonic_image,
                            source_linux_image=linux_image
                            )

    virtual_vm.cleanMemory()

    virtual_vm.defineLogicalInterfaces(logical_interfaces, 1, 40)
    virtual_vm.createLogicalInterfaces(65535)
    sleep(2)
    virtual_vm.defineLogicalInterfaces(dummy_interfaces, 1, 20)
    virtual_vm.createLogicalInterfaces()
    sleep(2)
    virtual_vm.createVirtualSonic('vrdc_info.csv')
    sleep(2)
    routers_config.configure_sonic_ztp()
    sleep(5)
    virtual_vm.createVirtualVms('vm_info.csv')
    sleep(5)
    routers_config.configure_virtual_router()


def delete_topology():

    print("#" * 150)
    print("#" * 100, "Delete Virtual Topology")

    virtual_vm = BasicInfra(source_sonic_image=sonic_image,
                            source_linux_image=linux_image
                            )

    virtual_vm.deleteVirtualLab('vrdc_info.csv')
    virtual_vm.deleteVirtualLab('vm_info.csv')
    sleep(2)
    virtual_vm.deleteSourceImages()
    sleep(2)
    virtual_vm.deleteInterface(logical_interfaces)
    virtual_vm.deleteInterface(dummy_interfaces)
    sleep(2)
    virtual_vm.cleanMemory()


if __name__ == "__main__":

    print("1 - Start Topology\n")
    print("2 - Stop Topology\n")
    print("3 - Create topology\n")
    print("4 - Delete topology\n")

    select_function = input("Select one Option: ") or None

    if select_function == '1':
        start_time = time.time()
        start_topology()
        run_time = time.time() - start_time
        run_time_min = run_time / 60
        print(f'Time to configure: {run_time_min}')
    elif select_function == '2':
        start_time = time.time()
        stop_topology()
        run_time = time.time() - start_time
        run_time_min = run_time / 60
        print(f'Time to configure: {run_time_min}')
    elif select_function == '3':
        print("Are you sure you want to create a topology from scratch?")
        select_function = input("Type 'yes' or 'no': ").upper() or None
        if select_function == 'YES' or None:
            start_time = time.time()
            create_topology()
            run_time = time.time() - start_time
            run_time_min = run_time / 60
            print(f'Time to configure: {run_time_min}')
            print("- Default user and password")
            print("- VMs: lab/lab123 and root/lab123, Sonic: admin/admin, Apstra: admin/admin")
        else:
            print("Wrong option!! Nothing to do!")
            exit()
    elif select_function == '4':
        print("Are you sure you want to delete everything?")
        select_function = input("Type 'yes' or 'no': ").upper() or None
        if select_function == 'YES' or None:
            start_time = time.time()
            delete_topology()
            run_time = time.time() - start_time
            run_time_min = run_time / 60
            print(f'Time to configure: {run_time_min}')
        else:
            print("Wrong option!! Nothing to do!")
            exit()
    else:
        print("Wrong option!! Nothing to do!")