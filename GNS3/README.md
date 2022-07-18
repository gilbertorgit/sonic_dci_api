# GNS3 environment

## Authors

**Gilberto Rampini**

## Topology

1. Topology, IP, and credentials remain the same, once GNS3 provides the same NAT Subnet Interface (192.168.122.0/24)
2. Make sure to connect your MGMT interface to this NAT Interface
3. CentOS Cloud Guest - https://gns3.com/marketplace/appliances/centos-cloud-guest
4. GNS3 allows you to upload .iso, please see the VM_ISO directory to automatically configure your hosts VMs
   1. C1-V10-H1 and C1-V10-H4 have 3 interfaces
      1. eth0 - no use
      2. eth1 - dc1/2-leaf-1
      3. eth2 - dc1/2-leaf-2
   2. All other VMs have 2 interfaces
      1. eth0 - no use
      2. eth1 - connected to leaf - See "main" topology

### GNS3 Topology - Print

<p align="center">
  DCI TOPOLOGY
  <img src="https://github.com/gilbertorgit/sonic_dci_api/blob/main/GNS3/GNS3PRINT.JPG">
</p>


## Basic Devices configuration - GNS3 Console Mode

This document provides basic info about GNS3 Environment

DC1
```
## default user/password
admin/YourPaSsWoRd

-------------------------------------------------------------------
sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin

sonic-cli
configure terminal

hostname dc1-sonic-spine-1

interface Management 0
ip address 192.168.122.215/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc1-sonic-spine-2

interface Management 0
ip address 192.168.122.216/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin

sonic-cli
configure terminal

hostname dc1-sonic-leaf-1

interface Management 0
ip address 192.168.122.217/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc1-sonic-leaf-2

interface Management 0
ip address 192.168.122.218/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc1-sonic-leaf-3

interface Management 0
ip address 192.168.122.219/24
no shutdown
end
write memory
exit
exit

-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc1-sonic-border-leaf-1

interface Management 0
ip address 192.168.122.220/24
no shutdown
end
write memory
exit
exit
```

DC2
```
## default user/password
admin/YourPaSsWoRd

-------------------------------------------------------------------
sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin

sonic-cli
configure terminal

hostname dc2-sonic-spine-1

interface Management 0
ip address 192.168.122.225/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc2-sonic-spine-2

interface Management 0
ip address 192.168.122.226/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin

sonic-cli
configure terminal

hostname dc2-sonic-leaf-1

interface Management 0
ip address 192.168.122.227/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc2-sonic-leaf-2

interface Management 0
ip address 192.168.122.228/24
no shutdown
end
write memory
exit
exit
-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc2-sonic-leaf-3

interface Management 0
ip address 192.168.122.229/24
no shutdown
end
write memory
exit
exit

-------------------------------------------

sudo config ztp disable -y 
## Change admin password – Password needs to be: admin
sudo passwd admin


sonic-cli
configure terminal

hostname dc2-sonic-border-leaf-1

interface Management 0
ip address 192.168.122.230/24
no shutdown
end
write memory
exit
exit
```

## SONIC API

You can still use Sonic API scripts to configure the entire topology.

In your GNS3 Shell:

```
gns3vm# apt -y install software-properties-common

gns3vm# add-apt-repository --yes ppa:deadsnakes/ppa

gns3vm# add-apt-repository --yes --update ppa:ansible/ansible

gns3vm# apt -y update

gns3vm# apt -y install ansible git

gns3vm# git clone https://github.com/gilbertorgit/sonic_dci_api.git
```

Change the playbook
```
gns3vm# vi sonic_dci_api/base-pkg-kvm/playbook.yml
```

Remove all the roles but python
```
--------------

---
  - name: Install Pyhon
    hosts: localhost
    roles:
      - python
---------------
```

Save and run the playbook
```
gns3vm# ansible-playbook sonic_dci_api/base-pkg-kvm/playbook.yml
```

Create Python venv and run the script
```
gns3vm# cd sonic_dci_api/

root@gns3vm:~/sonic_dci_api# python3.10 -m venv my-env

root@gns3vm:~/sonic_dci_api# source my-env/bin/activate

root@gns3vm:~/sonic_dci_api# pip install -r requirements.txt

root@gns3vm:~/sonic_dci_api# source my-env/bin/activate 

(my-env) root@gns3vm:~/sonic_dci_api#  cd sonic_api/
```

### Sonic API Configuration

* The script below will configure the entire topology using REST APIs
```
(my-env) root@gns3vm:~/sonic_dci_api/api_config# python main.py
```



