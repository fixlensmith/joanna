from netmiko import Netmiko
from datetime import datetime
from time import sleep


class Network:
    def __init__(self, username, password=None, keys=None):
        '''
        :param username: username of device
        :param password: password of device
        :param keys: boolean
        '''
        self.username = username
        self.password = password
        self.keys = keys

    def command_cisco(self, hosts, set_command):
        if hosts == 'bsd-asw-mgmt3' or hosts == 'bsd-asw-mgmt4':
            HOST = {
                    'ip' : hosts,
                    'username' : 'cisco-backup',
                    'password' : 'Cisco@Backup12#',
                    'device_type' : 'cisco_ios',
            }
        else:
            HOST = {
                    'ip' : hosts,
                    'username' : self.username,
                    'password' : self.password,
                    'use_keys' : self.keys,
                    'device_type' : 'cisco_ios',
            }
        net_connect = Netmiko(**HOST)
        return net_connect.send_command(set_command)


    def command_firewall(self, hosts, set_command):
        HOST = {
                'ip' : hosts,
                'username' : self.username,
                'password' : self.password,
                'use_keys' : self.keys,
                'device_type' : 'fortinet',
        }
        net_connect = Netmiko(**HOST)
        return net_connect.send_command(set_command)


    def config_cisco(self, host, set_command):
        HOST = {
                'ip' : host,
                'username' : self.username,
                'password' : self.password,
                'use_keys' : self.keys,
                'device_type' : 'cisco_ios',
        }
        net_connect = Netmiko(**HOST)
        return net_connect.send_config_set(set_command)


    def config_file(self, host, set_file):
        HOST = {
                'ip' : host,
                'username' : self.username,
                'password' : self.password,
                'use_keys' : self.keys,
                'device_type' : 'cisco_ios',
        }
        net_connect = Netmiko(**HOST)
        return net_connect.send_config_from_file(set_file)


    slb = ['slb-int-a', 'slb-int-b', 'slb-dmz-a', 'slb-dmz-b', 'slb-ext-a', 'slb-ext-b']


    firewall = ['bsd-fw','bsd-ext-fw']


    def config_file(self, device, command):
        sleep(1)
        net_connect = Netmiko(**device)
        net_connect.send_config_from_file(command)
        print( device['ip'] + ' Done')



    def backup(self):
        self.username = 'jefri'
        self.keys = True
        for host in ['bsd-core-a', 'bsd-core-b','bsd-dsw-a', 'bsd-dsw-b','bsd-banksw-a',
           'bsd-banksw-b','bsd-asw-ext-a', 'bsd-asw-ext-b','bsd-asw-dmz-a','bsd-asw-dmz-b',
           'bsd-asw-dev-a', 'bsd-asw-dev-b','bsd-asw-sync-a', 'bsd-asw-sync-b','bsd-rac-a',
           'bsd-rac-b','bsd-mgmt-sw1', 'bsd-mgmt-sw2']:
            file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}',"w")
            file.write(self.command_cisco(host, 'sh run'))
            sleep(3)
            file.close()


    def backup_slb(self):
        for host in ['slb-int-a', 'slb-int-b', 'slb-dmz-a', 'slb-dmz-b', 'slb-ext-a', 'slb-ext-b']:
            HOST = {
                'ip' : host,
                'username' : 'slb-backup',
                'password' : 'Nice@Backup12#',
                'device_type' : 'piolink',
        }
            net_connect = Netmiko(**HOST)
            sleep(1)
            file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}',"w")
            sleep(3)
            file.write(net_connect.send_command('show run'))
            file.close()


    def backup_fortigate(self):
        now = datetime.now()
        for host in ['bsd-fw','bsd-ext-fw']:
            HOST = {
                'ip' : host,
                'username' : 'jefri',
                'use_keys' : True,
                'device_type' : 'fortinet',
        }
            net_connect = Netmiko(**HOST)
            sleep(1)
            file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}',"w")
            file.write(net_connect.send_command('show full'))
            sleep(3)
            file.close()