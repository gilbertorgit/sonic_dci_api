# Using Virtual Sonic Enterprise 4.0.0 Powered by Dell and REST API to build a full DCI topology - (KVM environment)

## Authors

**Gilberto Rampini**

## Topology

<p align="center">
  <img
    src="https://github.com/gilbertorgit/sonic_dci_api/blob/main/topology_prints/DCI-TOPOLOGY.JPG"
  >
</p>
<p align="center">
  <img
    src="https://github.com/gilbertorgit/sonic_dci_api/blob/main/topology_prints/MGMT_IP.JPG"
  >
</p>

## Getting Started

This repository provides configuration examples for lab purposes only in order to help you get started with Virtual Enterprise Sonic Powered by Dell using Python and REST API.

* **This lab guide does not intend to cover any best practice and/or production configuration. All the configuration provided in this guide, are just "simple examples"**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

This project will make available:

1. Python script to create, start, stop and delete the entire topology
2. All the necessary steps to create a full lab using Virtual Sonic Enterprise Powered by Dell
3. Python scripts to create all Sonic configuration
4. Alternatively, there is a PDF document providing all steps to configure your entire topology
   1. If you are a Partner, contact your account manager to have access
   2. If you are an end customer, contact your partner to have access
6. Lab Topology

Following this guide, you will be able to build

1. DC1 - 3-Stage Clos network with Enterprise Sonic 4.0.0 using REST API to configure every single device
2. DC2 - 3-Stage Clos network with Enterprise Sonic 4.0.0 using REST API to configure every single device

Important Information
- The python script available in this guide will create and delete all resources as well as start and stop the entire topology.
- It's very important to keep the names and file paths as shown here otherwise, you're likely to face issues
- It's very important to keep the versions of the images, otherwise you are likely to face issues.   
- Default user and password: -> (You can change it by editing the python script)
  - root/lab123 
  - lab/lab123 
- Lab Network IP and Interface information:
  - 192.168.122.0/24 -> default KVM bridge network (You can change it by editing the python script)
  - virbr0 - default KVM bridge interface
    
## Prerequisites configs

This test lab has been built and tested using:

```
1. Ubuntu 18.04.5 LTS
2. Server with:
  2.1. 128GB RAM
  2.2. I9 with 14 Cores
  2.3. 500GB - SSD
3. Virtual Sonic Enterprise 4.0 - Powered by Dell
5. CentOS-7-x86_64-GenericCloud.qcow2
```

***Although we are downloading and copying packages and configurations within the /home/lab user directory, it's worth mentioning that I'm using root user access for every single step described here.***

## Pre-deployment Server Configs and Basic Packages

**Packages Installation and configuration**

```
lab@lab:~$ sudo su -

root@lab:~$ cd /home/lab

root@lab:/home/lab# apt -y install software-properties-common

root@lab:/home/lab# add-apt-repository --yes ppa:deadsnakes/ppa

root@lab:/home/lab# add-apt-repository --yes --update ppa:ansible/ansible

root@lab:/home/lab# apt -y update

root@lab:/home/lab# apt -y install ansible git

root@lab:/home/lab# git clone https://github.com/gilbertorgit/sonic_dci_api.git

root@lab:/home/lab# ansible-playbook sonic_dci_api/base-pkg-kvm/playbook.yml

root@lab:/home/lab/sonic_dci_api# cd sonic_dci_api/

root@lab:/home/lab/sonic_dci_api#  python3.10 -m venv my-env

root@lab:/home/lab/sonic_dci_api# source my-env/bin/activate

(my-env) root@lab:/home/lab/sonic_dci_api# pip install -r requirements.txt

(my-env) root@lab:/home/lab/sonic_dci_api# deactivate
```

**Change default virbr0 dhcp range from .254 to .100**
```
root@lab:/home/lab# virsh net-edit default

from:
<range start='192.168.122.2' end='192.168.122.254'/>
to
<range start='192.168.122.2' end='192.168.122.100'/>
```

**Reload your server to confirm all changes are working**

```
root@lab:/home/lab# shutdown -r now

root@lab:/home/lab# sudo su -

root@lab:~$ cd /home/lab
```

## Preparing the environment

### Download the images and copy to ent_sonic_apstra/sonic_3clos/images

* CentOS-7-x86_64-GenericCloud.qcow2 - https://cloud.centos.org/centos/7/images/

* Enterprise_SONiC_OS_3.3.0.img - https://www.dell.com/support/home/en-us/product-support/product/enterprise-sonic-distribution/drivers

```
root@lab:/home/lab# cp Enterprise_SONiC_OS_3.3.0.img CentOS-7-x86_64-GenericCloud.qcow2 /home/lab/sonic_dci_api/images/
```

***Make sure you download the right version as described in this guide. 
You will have a directory like that one:***

```
root@lab:/home/lab/# ls -l /home/lab/sonic_dci_api/images/

-rw-r--r-- 1 root root  858783744 Jan 14 08:55 CentOS-7-x86_64-GenericCloud.qcow2
-rw-r--r-- 1 root root 2473066496 Jan 14 08:55 Enterprise_SONiC_OS_4.0.0.img
-rw-r--r-- 1 root root 53 Jun 16 12:33 README.md
```

## Python Script

### Create Infrastructure

1. - Start Topology - It will start the entire topology (you have to create it first - Option 4)
2. - Stop Topology - It will stop the entire topology
3. - Create Topology - It will create the entire topology from scratch
4. - Delete Topology - It will delete and remove the entire topology and images

* In case you are running your environment under a vmware hypervisor, you have to run a guestfish workaround before this script:

```
root@lab:~# export LIBGUESTFS_BACKEND_SETTINGS=force_tcg
```

```
root@lab:~# cd /home/lab/sonic_dci_api/

root@lab:/home/lab/sonic_dci_api# source my-env/bin/activate

(my-env) root@lab:/home/lab/sonic_dci_api# python main.py
1 - Start Topology

2 - Stop Topology

3 - Create topology

4 - Delete topology

Select one Option:
```

## Sonic API Configuration Script

Before run the API Script, it's always good to check the management connectivity:

```
ping 192.168.122.215 -c 2
ping 192.168.122.216 -c 2
ping 192.168.122.217 -c 2
ping 192.168.122.218 -c 2
ping 192.168.122.219 -c 2
ping 192.168.122.220 -c 2
ping 192.168.122.225 -c 2
ping 192.168.122.226 -c 2
ping 192.168.122.227 -c 2
ping 192.168.122.228 -c 2
ping 192.168.122.229 -c 2
ping 192.168.122.230 -c 2
```

In case you face any issues, you can configure it manually:
```
 Id    Name                           State
----------------------------------------------------
 45    lab3-dc1-sonic-leaf-1          running
 46    lab3-dc1-sonic-leaf-2          running
 47    lab3-dc1-sonic-leaf-3          running
 48    lab3-dc1-sonic-spine-1         running
 49    lab3-dc1-sonic-spine-2         running
 50    lab3-dc1-sonic-borderleaf-1    running
 51    lab3-dc2-sonic-leaf-1          running
 52    lab3-dc2-sonic-leaf-2          running
 53    lab3-dc2-sonic-leaf-3          running
 54    lab3-dc2-sonic-spine-1         running
 55    lab3-dc2-sonic-spine-2         running
 56    lab3-dc2-sonic-borderleaf-1    running
 57    lab3_c1_v10_h1                 running
 58    lab3_c1_v10_h2                 running
 59    lab3_c1_v20_h3                 running
 60    lab3_c2_v100_h1                running
 61    lab3_c2_v200_h2                running
 62    lab3_c1_v10_h4                 running
 63    lab3_c1_v10_h5                 running
 64    lab3_c1_v30_h6                 running
 65    lab3_c2_v100_h3                running
 66    lab3_c2_v300_h4                running


* admin/admin (or YourPaSsWoRd -> Default Sonic Password)
root@lab:# virsh console dc1-sonic-leaf-1

* Disable ZTP
# sudo config ztp disable

* configures admin as password
# sudo passwd admin
Enter new: admin
Enter new: admin

# sonic-cli
# configure terminal

* Based on topology names
# hostname <hostname> 

# interface Management 0
# ip address 192.168.122.217/24
# no shutdown
# exit
# exit
# write memory
# exit
# exit
```

* The script below will configure the entire topology using REST APIs
```
root@lab:# cd /home/lab/sonic_dci_api/sonic_api/

root@lab:/home/lab/sonic_dci_api/sonic_api# python main.py
```

**You can check some scripts output in the folder "Output_Script_Example**

## Customer VMs Access

* Default user and password: lab/lab123

```
root@lab:# virsh console <VM_NAME>

root@lab:# virsh console c1_v10_h1
```