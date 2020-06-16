import os

import pexpect
from Crypto.PublicKey import RSA


class KeyRegistrationHelper:

    def __init__(self, user, password):
        self.key_path = ".key"
        if not os.path.exists(self.key_path):
            os.makedirs(self.key_path)
        self.generate_ssh_key()
        self.user = user
        self.pw = password
        self.logs = open('.out/register-ssh-logs.txt', 'wb')

    def generate_ssh_key(self):
        key = RSA.generate(2048)
        with open(F"{self.key_path}/id_rsa", 'wb') as content_file:
            os.chmod(F"{self.key_path}/id_rsa", 0o600)
            content_file.write(key.exportKey('PEM'))
        pubkey = key.publickey()
        with open(F"{self.key_path}/id_rsa.pub", 'wb') as content_file:
            content_file.write(pubkey.exportKey('OpenSSH'))

    # used for linux ssh connections only
    def register_ssh_key_on_host(self, host):
        self.register_key(host)
        self.test_ssh_with_key(host)

    # Use ssh-copy-id to register the local key on a remote host
    def register_key(self, ip):
        child = pexpect.spawn(
            F'ssh-copy-id'
            F' -i {self.key_path}id_rsa'
            F' {self.user}@{ip}'
            F' -o StrictHostKeyChecking=no -f')
        child.logfile_read = self.logs

        i = child.expect(['password'])
        if i == 0:
            print('Wants to know PW')
        else:
            child.sendline('yes')

        added_key = False
        while not added_key:
            child.sendline(self.pw)
            i = child.expect(['added:', 'denied'])
            if i == 0:  # Key successfully added
                added_key = True
            if i == 1:  # Permission denied
                child.close()
                raise PermissionError(
                    'SSH connection denied because of permission issues')
        child.close()

    # connect to the host via ssh and closes the connection afterwards
    def test_ssh_with_key(self, ip):
        child = pexpect.spawn(
            F"ssh -i"
            F" {self.key_path}id_rsa"
            F" -o 'StrictHostKeyChecking=no'"
            F" {self.user}@{ip}")
        child.logfile_read = open('.out/register-ssh-logs.txt', 'wb')

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

    # connect to the host via ssh and remove ssh key
    def remove_ssh_key(self, ip):
        child = pexpect.spawn(
            F"ssh -i {self.key_path}id_rsa"
            F" -o 'StrictHostKeyChecking=no'"
            F"  {self.user}@{ip}")
        child.logfile_read = open('.out/register-ssh-logs.txt', 'wb')

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

    def ssh_key_delete_cmd(self):
        key = open(F"{self.key_path}id_rsa.pub", "r").read().rstrip()

        # split the key in its three parts (ssh-rsa, content, name)
        key_parts = key.split(' ')

        # TODO: Command should also replace newline
        return F"sed -i.bak '/{key_parts[0]}.*{key_parts[2]}/ g'" \
               F" .ssh/authorized_keys" \
               F" && exit"
