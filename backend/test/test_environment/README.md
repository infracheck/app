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
docker run -d -p 8899:20 --name ubuntu-sshd ubuntu-sshd
```

### Windows Server 2016:
Vagrantfile launches windows server 2016 vm with winrm.

**Requirements**
- Vagrant
- Virtualbox

**Credentials**
- username: root
- password: password

**Deployment:**
```
docker build -t ubuntu-sshd .
docker run -d -p 8899:20 --name ubuntu-sshd ubuntu-sshd
```
