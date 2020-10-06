# InfraCheck - Offline Guide
## Purpose of this document
This document provides a tutorial for infracheck to install it on offline systems.

## Description
Often, customer systems operate behind firewalls or have no internet access at all. 
This can lead to problems, because **InfraCheck** follows a plugin principle. 
Therefore, it loads the plugin dependencies during runtime. 
The idea behind this offline apporach is, to start the service in a local container.
Create an image of that container next and push it to the target system without internet access.

## Perquisites
* Docker and `docker-compose` on your target system [Installation Guide](https://docs.docker.com/get-docker/)
* Docker and `docker-compose` on your local system (with internet access)

> You can do everything without docker-compose but it makes life more easier.
> Without it, you need to configure docker networking on your own.

## Guide
1: Launch all containers using `docker-compose up -d`
2: Create images of the running containers:
```commandline
docker commit infra-backend infra-backend
docker commit infra-frontend infra-frontend
docker commit infra-reverse infra-reverse
```
Everything worked if you have the following images:
```commandline
$ docker images
REPOSITORY              TAG                 IMAGE ID            CREATED              SIZE
infra-reverse           latest              37bc4fc04f41        5 seconds ago        22.1MB
infra-backend           latest              a0814bbe201b        14 seconds ago       1.01GB
infra-frontend          latest              591bf08ad484        About a minute ago   1.39GB
```
3: Save the images as a `tar` file
```commandline
docker save infra-reverse > infra-reverse.tar
docker save infra-backend > infra-backend.tar
docker save infra-frontend > infra-frontend.tar
```
4: Move those files to your target system (scp, ftp, usb stick, ...)
5: Load the compressed images
```commandline
docker load --input infra-reverse.tar
docker load --input infra-backend.tar
docker load --input infra-frontend.tar
```
There are the images:
```commandline
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
infra-frontend      latest              aaab9391a85c        3 minutes ago       1.39GB
infra-backend       latest              66bf832cf0b9        3 minutes ago       1.01GB
infra-reverse       latest              41eb69a6bbdc        3 minutes ago       22.3MB
```
6: Simply launch the containers using the following `docker-compose.yml` and `docker-compose up -d`:
```yml
version: '3'
services:
  frontend:
    container_name: infra-frontend
    image: infra-frontend
  backend:
    container_name: infra-backend
    image: infra-backend
  reverse:
    container_name: infra-reverse
    image: infra-reverse
    ports:
      - 80:80
      - 443:443
```
