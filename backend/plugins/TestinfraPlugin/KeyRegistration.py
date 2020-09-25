import os
from typing import List

import pexpect

from infracheck import log
from plugins.TestinfraPlugin.Configuration import Configuration


class KeyRegistration:
    """
    This class can be used to register your ssh key at the remote host
    This is needed by the testinfra plugin.
    To test linux machines via ssh testinfra only supports key based authentication.
    """

    def __init__(self, user, password, port=22):
        """
        Create new ssh key every launch
        :param user:
        :param password:
        """
        self.user = user
        self.pw = password
        self.port = port
        # Create ssh key
        if not os.path.exists(Configuration.SSH_FOLDER):
            os.makedirs(F"{Configuration.SSH_FOLDER}")
        if os.path.isfile(F"{Configuration.SSH_FOLDER}id_rsa"):
            os.remove(F"{Configuration.SSH_FOLDER}id_rsa")
            os.remove(F"{Configuration.SSH_FOLDER}id_rsa.pub")
        os.system(F"ssh-keygen -m pem -q -t rsa -N '' -f {Configuration.SSH_FOLDER}id_rsa")

    # subprocess.run(F"ssh-keygen -q -t rsa -N '' -f {Configuration.SSH_FOLDER}id_rsa <<< y", shell=True, check=True)

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
            F' -p {self.port}'
            F' -i {Configuration.SSH_FOLDER}id_rsa'
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
                log.info("Key successfully added")

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
            F" {Configuration.SSH_FOLDER}id_rsa"
            F" -o 'StrictHostKeyChecking=no'"
            F" {self.user}@{ip}"
            F" -p {self.port}"
        )
        child.logfile_read = open(F'{Configuration.SSH_FOLDER}register-ssh-logs.txt', 'wb')

        i = child.expect(['login:'])
        if i == 0:
            child.sendline('exit')
            i = child.expect(['closed'])
            if i == 0:
                log.info("Logout successful")
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
            F"ssh -i {Configuration.SSH_FOLDER}id_rsa"
            F" -p {self.port}"
            F" -o 'StrictHostKeyChecking=no'"
            F"  {self.user}@{ip}")
        child.logfile_read = open(F'{Configuration.SSH_FOLDER}register-ssh-logs.txt', 'wb')

        i = child.expect(['login:'])
        if i == 0:
            child.sendline(self.ssh_key_delete_cmd())
            i = child.expect(['closed'])
            if i == 0:
                log.info("Logout successful")
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
        key = open(F"{Configuration.SSH_FOLDER}id_rsa.pub", "r").read().rstrip()

        # split the key in its three parts (ssh-rsa, content, name)
        key_parts = key.split(' ')

        # TODO: Command should also replace newline
        return F"sed -i.bak '/{key_parts[0]}.*{key_parts[2]}/ g'" \
               F" .ssh/authorized_keys" \
               F" && exit"
