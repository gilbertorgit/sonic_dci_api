"""
---------------------------------
 Author: Gilberto Rampini
 Date: 18/06/2022
---------------------------------
"""

import logging
import pexpect
from shlex import quote
from time import sleep

user = "admin"
pwd = "YourPaSsWoRd"
new_pwd = "admin"
admin_prompt = 'admin@sonic:~[$]'


def config_virtual_sonic_ztp(hostname):
    print("-" * 60)
    print(f"- {hostname}: Disabling Sonic ZTP")

    child = pexpect.spawn(f"virsh console {quote(hostname)} --force", timeout=200, maxread=4000)
    logging.debug("Got console, Logging in as admin")
    child.send("\r\r\r")

    child.expect(".*login:")
    logging.debug(f"sending user: {user}")
    child.sendline(user)

    child.expect("Password:")
    logging.debug(f"sending user: {pwd}")
    child.sendline(pwd)

    child.send("\r")
    child.expect(admin_prompt)
    logging.debug("disabling ZTP")
    child.sendline("sudo config ztp disable -y")
    print("1")
    child.expect("Verifying if core services have started", timeout=300)
    print("2")
    child.send("\r")
    print("3")
    child.expect(admin_prompt, timeout=300)
    print(f"- {hostname}: ZTP Finished")
    child.sendline("exit")
    child.send("\r")
    print(f"- {hostname}: Leaving Console")
    child.sendcontrol("]")

    print(f"- {hostname}: ZTP disabled - completed")


def config_virtual_sonic(hostname, mgmt_ip):
    print("-" * 60)
    print(f"- {hostname}: Configuring  with MGMT IP: {mgmt_ip}")

    child = pexpect.spawn(f"virsh console {hostname} --force", timeout=200, maxread=4000)

    logging.debug("Got console, Logging in as admin")
    child.send("\r\r\r")

    child.expect(".*login:")
    logging.debug(f"sending user: {user}")
    child.sendline(user)

    child.expect("Password:")
    logging.debug(f"sending user: {pwd}")
    child.sendline(pwd)
    child.send("\r")

    print(f"- {hostname}: changing admin password to : admin")
    child.expect("admin\@.*")
    child.send("\r")
    logging.debug("Sending cli")
    child.sendline("sudo passwd admin")
    child.expect("New password:")
    child.sendline(new_pwd)
    child.expect("Retype new password:")
    child.sendline(new_pwd)
    child.send("\r")
    print(f"- {hostname}: admin password done!")

    print(f"- {hostname}: Sonic-CLI Mode")
    child.expect("admin\@.*")
    logging.debug("Sending cli")
    child.sendline("sonic-cli")
    child.send("\r")
    child.expect("sonic")
    logging.debug("Sending configure")
    child.sendline("configure terminal")
    child.expect("sonic\(config\)")

    print(f"- {hostname}: Configuring interface-naming standard")
    logging.debug("configuring interface-naming standard")
    child.sendline("interface-naming standard")
    child.send("\r")
    child.expect("sonic\(config\)")

    print(f"- {hostname}: Configuring Management Interface: {mgmt_ip}")
    logging.debug("going to interface MGMT")
    child.sendline("interface Management 0")
    child.expect("sonic\(conf\-if\-eth0\)")
    logging.debug("configuring interface MGMT")
    child.sendline(f"ip address {mgmt_ip}/24")
    child.expect("sonic\(conf\-if\-eth0\)")
    child.sendline("exit")

    print(f"- {hostname}: Configuring hostname: {hostname} ")
    child.expect("sonic\(config\)")
    child.sendline(f"hostname {hostname}")
    child.send("\r")
    child.send("\r")

    print(f"- {hostname}: Saving configuration")
    child.expect("sonic\(config\)")
    child.send("\r")
    child.sendline("write memory")
    child.send("\r")

    child.expect("sonic\(config\)")
    child.sendline("exit")

    child.expect("sonic")
    child.sendline("exit")

    child.expect("admin\@.*")
    child.sendline("exit")
    child.send("\r")
    child.sendcontrol("]")

    print(f"- {hostname}: configuration completed")


if __name__ == "__main__":

    config_virtual_sonic_ztp('test_sonic_4')
    #config_virtual_sonic('test_sonic_4', '192.168.0.215')

