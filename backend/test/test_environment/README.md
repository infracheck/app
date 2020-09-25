# Test environments
This directory contains test environments / distributions for InfraCheck, that can be used to test SSH and WINRM connection backends.
## Currently working
### Ubuntu 16:
Dockerfile launches an ubuntu container with ssh enabled.

**Requirements**
- Docker

**Credentials**
- username: root
- password: password

**Deployment:**
```
docker build -t ubuntu-sshd .
docker run -dt -p 8899:22 --name ubuntu-sshd ubuntu-sshd
# Get IP adress
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ubuntu-sshd
```

### Windows Server 2016:
Vagrantfile launches windows server 2016 vm with winrm.

**Requirements**
- Vagrant
- Virtualbox

**Credentials**
- username: vagrant
- password: vagrant
- address: 192.168.200.200
- port: 5985

**Deployment:**
```
vagrant up
connect to winrm://vagrant:vagrant@192.168.200.200:5985?no_ssl=true&no_verify_ssl=true
```
