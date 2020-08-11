import os
import subprocess
from typing import List

import pexpect

from plugins.testinfra.Config import Config


class KeyRegistrationHelper:
    """
    This class can be used to register your ssh key at the remote host
    This is needed by the testinfra plugin.
    To test linux machines via ssh testinfra only supports key based authentication.
    """

    def __init__(self, user, password):
        """
        Create new ssh key every launch
        :param user:
        :param password:
        """
        # Create ssh key
        if not os.path.exists(Config.SSH_FOLDER):
            os.makedirs(Config.SSH_FOLDER)
        subprocess.run(F"echo -e 'y\n' | ssh-keygen -q -t rsa -N '' -f {Config.SSH_FOLDER}id_rsa",
                       shell=True,
                       check=True)
        self.user = user
        self.pw = password

    def register_ssh_keys(self, hosts: List[str]):
        """
        Register ssh key for every given host
        :param hosts:
        :return:
        """
        for host in hosts:
            self.register_ssh_key_on_host(host)

    def clean_ssh_keys(self, hosts: List[str]):
        """
        Remove ssh keys on every given host
        :param hosts:
        :return:
        """
        for host in hosts:
            self.remove_ssh_key(host)

    def register_ssh_key_on_host(self, host):
        """
        used for linux ssh connections only
        :param host:
        :return:
        """
        self.register_key(host)
        self.test_ssh_with_key(host)

    def register_key(self, ip):
        """
        Use ssh-copy-id to register the local key on a remote host
        :param ip:
        :return:
        """
        child = pexpect.spawn(
            F'ssh-copy-id'
            F' -i {Config.SSH_FOLDER}id_rsa'
            F' {self.user}@{ip}'
            F' -o StrictHostKeyChecking=no -f')

        i = child.expect(['password', 'added:'])
        added_key = False
        if i == 0:
            child.sendline(self.pw)
        if i == 1:
            added_key = True
        else:
            child.sendline('yes')

        while not added_key:
            child.sendline(self.pw)
            i = child.expect(['added:', 'denied'])
            if i == 0:  # Key successfully added
                added_key = True
                print("Key successfully added")

            if i == 1:  # Permission denied
                child.close()
                raise PermissionError(
                    'SSH connection denied because of permission issues')
        child.close()

    def test_ssh_with_key(self, ip):
        """
        connect to the host via ssh and closes the connection afterwards
        :param ip:
        :return:
        """
        child = pexpect.spawn(
            F"ssh -i"
            F" {Config.SSH_FOLDER}id_rsa"
            F" -o 'StrictHostKeyChecking=no'"
            F" {self.user}@{ip}")
        child.logfile_read = open(F'{Config.OUTPUT_FOLDER}register-ssh-logs.txt', 'wb')

        i = child.expect(['login:'])
        if i == 0:
            child.sendline('exit')
            i = child.expect(['closed'])
            if i == 0:
                print("Logout successful")
            else:
                raise ConnectionError('Logout after ssh failed')
        else:
            raise ConnectionError('Could not login via ssh')
        child.close()

    def remove_ssh_key(self, ip):
        """
        connect to the host via ssh and remove ssh key
        :param ip:
        :return:
        """
        child = pexpect.spawn(
            F"ssh -i {Config.SSH_FOLDER}id_rsa"
            F" -o 'StrictHostKeyChecking=no'"
            F"  {self.user}@{ip}")
        child.logfile_read = open(F'{Config.OUTPUT_FOLDER}register-ssh-logs.txt', 'wb')

        i = child.expect(['login:'])
        if i == 0:
            child.sendline(self.ssh_key_delete_cmd())
            i = child.expect(['closed'])
            if i == 0:
                print("Logout successful")
            else:
                raise ConnectionError('Problem overwriting authorized keys')
        else:
            raise ConnectionError('Could not login via ssh')
        child.close()

    @staticmethod
    def ssh_key_delete_cmd():
        """
        Create command to remove the ssh_key from remote host
        :return:
        """
        key = open(F"{Config.SSH_FOLDER}id_rsa.pub", "r").read().rstrip()

        # split the key in its three parts (ssh-rsa, content, name)
        key_parts = key.split(' ')

        # TODO: Command should also replace newline
        return F"sed -i.bak '/{key_parts[0]}.*{key_parts[2]}/ g'" \
               F" .ssh/authorized_keys" \
               F" && exit"