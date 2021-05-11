# MaintenaceAid
=========

Thermography and vibrations web app assistant

[![Build Status](https://travis-ci.org/OpenDroneMap/WebODM.svg?branch=master)](https://travis-ci.org/OpenDroneMap/WebODM) 

A user-friendly, software for thermograph image and vibtrations chart processing, Generate status report of machinery in seconds not hours.

![image](https://ibb.co/dkhCtgp)

* [Getting Started](#getting-started)
* [Where Are My Files Stored?](#where-are-my-files-stored)
* [Setting Up Your Users](#setting-up-your-users)
* [Backup and restore](#backup-and-restore)
* [Recommended Machine Specs](#recommended-machine-specs)

![image](https://ibb.co/ZGskc7d)

![image](https://ibb.co/p1bPdLy)

## Getting Started
--------------

To install MaintenanceAid, follow these steps to get you up and running:

* Install the following applications (if they are not installed already):
  - [Git](https://git-scm.com/downloads)
  - [Docker](https://www.docker.com/)
  - [Docker-compose](https://docs.docker.com/compose/install/)
  - Python
  - Pip

* Windows users should install [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows) and:
  1. Make sure Linux containers are enabled (Switch to Linux Containers...)
  1. Give Docker enough CPUs (default 2) and RAM (>4Gb, 16Gb better but leave some for Windows) by going to Settings -- Advanced
  1. Select where on your hard drive you want virtual hard drives to reside (Settings -- Advanced -- Images & Volumes)

* From the Docker Quickstar Terminal or Git Bash (Windows), or from the command line (Mac / Linux), type:
```bash
git clone https://github.com/p1gm1/MaintenanceAid.git
cd MaintenaceAid
sudo docker-compose -f local.yml build
sudo docker-compose -f local.yml up
```

* If you don't wanna use the sudo command, make sure your user is part of the docker group:
```bash
sudo usermod -aG docker $USER
exit
(restart shell by logging out and then back-in)
docker-compose -f local.yml build
docker-compose -f local.yml up
```
* Open a web browser to `http://localhost:8000` (unless you are on Windows using Docker Toolbox, see below)

Docker Toolbox users need to find the IP of their docker machine by running this command from the Docker Quickstart Terminal:
```bash
docker-machine ip
192.168.1.100 (your output will be different)
```

The address to connect to would then be: `http://192.168.1.100:8000`.

To stop MaintenaceAid press CTRL+C or run:

```bash
sudo docker-compose -f local.yml down
```
We recommend that you read the [Docker Documentation](https://docs.docker.com/) to familiarize with the application lifecycle, setup and teardown, or for more advanced uses.

## Where Are My Files Stored?
--------------

When using Docker, all processing results are stored in a docker volume and are not available on the host filesystem.

## Setting Up Your Users
--------------

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

* To create a **super user**, type in a console the following:
```bash
sudo docker-compose -f local.yml run --rm django python3 manage.py createsuperuser
```

## Backup and Restore
--------------

If you want to move MaintenanceAid to another ssytem, you just need to trnasfer the docker volumes.

On the old system:
```bash
mkdir -v backup
sudo docker run --rm --volume maintenaceaid_dbdata:/temp --volume `pwd`/backup:/backup ubuntu tar cvf /backup/dbdata.tar /temp
docker run --rm --volume maintenaceaid_appmedia:/temp --volume `pwd`/backup:/backup ubuntu tar cvf /backup/appmedia.tar /temp
```

Your backup files will be stored in the newly created `backup` directory. Transfer the `backup` directory to the new system, then on the new system:
```bash
ls backup # --> appmedia.tar  dbdata.tar
sudo docker-compose -f local.yml down # Make sure maintenaceaid is down
docker run --rm --volume maintenaceaid_dbdata:/temp --volume `pwd`/backup:/backup ubuntu bash -c "rm -fr /temp/* && tar xvf /backup/dbdata.tar"
docker run --rm --volume maintenaceaid_appmedia:/temp --volume `pwd`/backup:/backup ubuntu bash -c "rm -fr /temp/* && tar xvf /backup/appmedia.tar"
sudo docker-compose -f local.yml up
```

## Recommended Machine Specs
--------------
To run MaintenaceAid, including the deep learning model, we recommend at a minimum:

* 100GB free disk space
* 16GB RAM
* GPU cuda compatible

However if you don't have a GPU it will still work, it just will be slow.

MaintenaceAid runs best on Linux, but works well on Windows and Mac too. if you are technically inclined, you can get to run natively on all three plataforms and there's a [native installer for Ubuntu 16.04](https://www.opendronemap.org/webodm/server-installer/) also available.

## License
--------------
MaintenaceAid is licensed under MIT License.

