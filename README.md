# Distribut.io






# Architecture 

## Distribut.io 
<img width="749" alt="Screen Shot 2023-01-23 at 7 24 48 PM" src="https://user-images.githubusercontent.com/13450068/214107343-13b94f68-a5d5-4250-910e-a17d052d283f.png">

## Tunnel 
![image](https://user-images.githubusercontent.com/13450068/214107042-fa82df1c-4507-411e-91eb-be6e40e6f650.png)


## BOINC 

![Test](https://upload.wikimedia.org/wikipedia/commons/9/94/Boincarchitecture.png)

## OpenStack

### OpenStack Resource Sharing Architecture 
![image](https://user-images.githubusercontent.com/13450068/214103251-0c74535f-697e-4f9c-af53-bfe010fd6443.png)

### OpenStack Services
![image](https://www.freecodecamp.org/news/content/images/2022/04/openstack-map.svg)


# Installation 

## Tunnel (based on tunnel.pyjam.as)

Public instance: [https://tunnel.pyjam.as/](https://tunnel.pyjam.as/)

`tunnel.pyjam.as` can be used as an ephemeral reverse proxy for your local
services.

`tunnel.pyjam.as` works without installing any software on your machine,
thanks to the magic of Wireguard.

Alternative Tunnels : https://github.com/anderspitman/awesome-tunneling

### Usage

To start a tunnel for your local service on port 8080
> Remember to bind your local service to 0.0.0.0

```
curl https://tunnel.pyjam.as/8080 > tunnel.conf && wg-quick up ./tunnel.conf
```

To stop your tunnel

```
wg-quick down ./tunnel.conf
```


### Self-hosting

Requirements: `python >= 3.9`, `poetry`, `wireguard`, `caddy`.

Use `poetry` to install the dependencies. There is a systemd service
included in the repository as well.


## OpenStack

These instructions use MicroStack ‐ in a snap. MicroStack is a pure upstream OpenStack distribution, designed for small scale and edge deployments, that can be installed and maintained with a minimal effort.

NOTE: MicroStack is in a beta state. We encourage you to test it, give us your feedback and ask questions.
Installation
The installation step consists solely of installing the MicroStack snap.

### Requirements

You will need a multi-core processor and at least 8 GiB of memory and 100 GiB of disk space. MicroStack has been tested on x86-based physical and virtual (KVM) machines running either Ubuntu 18.04 LTS or Ubuntu 20.04 LTS.

At this time use the beta channel:

`sudo snap install microstack --beta`

Install the snap on the machine designate as the control node and on any machines designated as compute nodes.

Information on the installed snap can be viewed like this:

`snap list microstack`


### Initialisation
Both the control node and the compute nodes must be initialised.

### Control node
Perform this step on the machine designated as the control node.

The control node initialisation step automatically deploys, configures, and starts OpenStack services. In particular, it will create the database, networks, an image, several flavors, and ICMP/SSH security groups. This can all be done within 10 to 20 minutes depending on your machine:

`sudo microstack init --auto --control`

When finished, generate a connection string that a designated compute node will need in order to join the cluster:


### Compute node
Perform this step on a machine designated as a compute node using the previously generated connection string.

Since the compute node only manages the OpenStack compute service a compute node’s initialisation step is much shorter than that of a control node’s. It can take as little as 30 seconds for a compute node to join the cluster:

`sudo microstack init --auto --compute --join <connection-string>`

Note:
Each additional compute node will require a new connection string to be generated. Add as many compute nodes as desired by repeating the join process.

### Verification 

The purpose of the verification step is to confirm that the cloud is in working order and to discover some of the defaults used by MicroStack. Verification will consist of the following actions:

- perform various OpenStack queries
- create an instance
- connect to the instance over SSH
- access the cloud dashboard
- Query OpenStack

The commands in this section can be invoked on either the control node or on a compute node.

The standard openstack client comes pre-installed and is invoked like so:

`microstack.openstack <command>`

To list the default image:

`microstack.openstack image list`


To get the default list of flavors:

`microstack.openstack flavor list`

Create an instance
The commands in this section can be invoked on either the control node or on a compute node.

MicroStack comes with a convenient instance creation command called microstack launch. It uses the following defaults for its instances:

keypair ‘microstack’
flavor ‘m1.tiny’
floating IP address on subnet ‘10.20.20.0/24’
The instance will be created on a compute node that the creating node sees as an availability zone, which in turn is based on hypervisor names.

To get the list of hypervisors:

microstack.openstack hypervisor list


There should be at least two. One that is bundled with the control node and one for each compute node.

Important:
To create an instance from a compute node you will need to first manually import an OpenStack keypair (i.e. ssh-keygen and microstack.openstack keypair create).

From the control node, to create an instance (on hypervisor ‘pmatulis-ss-mstack-2’) named ‘test’ that is based on the ‘cirros’ image:

microstack launch cirros --name test --availability-zone nova:pmatulis-ss-mstack-2.project.serverstack
The microstack launch command also supports arguments --key, --flavor, --image, and --net-id, in which case you will need to create objects using the standard client if non-default values are desired.

Note:
The launch command can be replaced with the traditional microstack.openstack server create command.

Connect to the instance
Output from the microstack launch command includes all the information needed to connect to the instance over SSH:

Creating local "microstack" ssh key at /home/ubuntu/snap/microstack/common/.ssh/id_microstack
Launching server ...
Allocating floating ip ...
Server test launched! (status is BUILD)

Access it with `ssh -i /home/ubuntu/snap/microstack/common/.ssh/id_microstack cirros@10.20.20.204`

**Important:**

When connecting to the instance over SSH from a compute node, OpenStack security groups will need to be configured.

From the control node, access the instance using the private SSH key associated with the default keypair:

`ssh -i /home/ubuntu/snap/microstack/common/.ssh/id_microstack cirros@10.20.20.204`

Note:

If you receive the error message sign_and_send_pubkey: no mutual signature supported then you will need to use the PubkeyAcceptedKeyTypes option to allow for older key types. The complete command will look like this: `ssh -o "PubkeyAcceptedKeyTypes +ssh-rsa" -i /home/ubuntu/snap/microstack/common/.ssh/id_microstack cirros@10.20.20.204`

### Access the cloud dashboard

You can log in to the web UI by pointing your browser to the following URL:

https://10.20.20.1

The username is ‘admin’ and the password is obtained in this way:

`sudo snap get microstack config.credentials.keystone-password`



## BOINC 


### Requirements

If you are hosting your server on a Linux machine, the requirements are,

* [Docker](https://docs.docker.com/engine/installation/) (>=17.03.0ce)
* [docker-compose](https://docs.docker.com/compose/install/) (>=1.13.0 but !=1.19.0 due to a [bug](https://github.com/docker/docker-py/issues/1841))
* git

(Note that Docker requires a 64-bit machine and Linux kernel newer than version 3.10)

If your are hosting your server on Windows/Mac, you should use either,

* [Docker for Mac](https://docs.docker.com/docker-for-mac/install/#download-docker-for-) (>=17.06.0ce)
* [Docker for Windows](https://docs.docker.com/docker-for-windows/install/) (>=17.06.0ce)

If you Windows/Mac system is too old to run either of those, you can use instead, 

* [Docker Toolbox](https://docs.docker.com/toolbox/overview) (>=17.05.0ce)

There are no other dependencies, as everything else is packaged inside of Docker. 

The server itself runs Linux. On Windows/Mac, Docker does the job of transparently virtualizing a Linux machine for you. The commands given in this guide should be run from your system's native terminal, unless you are running Docker Toolbox, in which case they should be run from the "Docker Quickstart Terminal" (and on Windows you will need to add `.exe` to the end, e.g. `docker.exe` instead of `docker`).

### Launching a test server

Before creating your real project, lets launch a sample test server to see how it works. To do this, get the `boinc-server-docker` source code, 

```bash
git clone https://github.com/marius311/boinc-server-docker.git
cd boinc-server-docker
```

and then run,

```bash
docker-compose pull
docker-compose up -d
```

You now have a running BOINC server! 

> *Notes:* 
> * The first time you run this, it may take a few minutes after invoking the `docker-compose up -d` command before the server webpage appears. 
> * Make sure your user is added to the `docker` group, otherwise the `docker-compose` and `docker` commands in this guide need to be run with `sudo`. 
> * If using Docker Toolbox, replace the final command above with `URL_BASE=$(docker-machine ip) docker-compose up -d`. The server will be accessible at the IP returned by `docker-machine ip` rather than at `127.0.0.1`.
The server is made up of three Docker images,

* **boinc/server_mysql** - This runs the MySQL server that holds your project's database. The database files are stored inside a volume called "boincserverdocker_mysql"
* **boinc/server_apache** - This runs the Apache server that serves your project's webpage. It also runs all of the various backend daemons and programs which communicate with hosts that connect to your server.
* **boinc/server_makeproject** - Unlike the other two images, this one doesn't remain running while your server is running. Instead, its run at the beginning to create your project's home folder. Your project's home folder contains things like your web pages, your applications, your job input files, etc... This folder is stored in a volume "boincserverdocker_project" and is mounted into the apache image after its created by this image.

The `docker-compose` program orchestrates Docker applications which involve multiple Docker images (like ours). The configuration and relation between the multiple images can be seen in the file `docker-compose.yml`. 

If you wish to get a shell inside your server (sort of like ssh'ing into it), run `docker-compose exec apache bash`. From here you can run any one-time commands on your server, for example checking the server status (`bin/status`) or submitting some jobs with (`bin/create_work ...`; more on this later). However, remember that only the project folder is a volume, so any changes you make outside of this will disappear the next time you restart the server. In particular, any software installed with `apt-get` will disappear; the correct way to install anything into your server is discussed [later](tbd). 


### Server URL

BOINC servers have their URL hardcoded, and will not function correctly unless they are actually accessible from this URL on the computer your are testing them from. By default, `boinc-server-docker` takes server URL to be `https://127.0.0.1`, i.e. localhost. If you are running Docker natively and testing on your local machine this is the correct URL and you don't need to take any other action. 

If this is not the case, for example if you are running Docker via Docker Machine instead of natively, or if you are running the server remotely, you will have to change the server URL. You can do so with the following command,

```bash
URL_BASE=http://1.2.3.4 docker-compose up -d
```

where you can replace `http://1.2.3.4` with whatever IP address or hostname you want to set for your server. 

Note that each time you run the `docker-compose up` command you should specify the `URL_BASE` otherwise it will reset to the default. If you are running via Docker Machine, you can use `URL_BASE=http://$(docker-machine ip)` to automatically set the correct URL. 

At this point, your BOINC server is now 100% fully functioning, its webpage can be accessed at `http://127.0.0.1/boincserver` or whatever you have set the server URL, and it is ready to accept connections from clients and submission of jobs. 


### Running jobs

Traditionally, creating a BOINC application meant either compiling your code into static binaries for each platform you wanted to support (e.g. 32 and 64-bit Linux, Windows, or Mac), or creating a Virtualbox image housing your app. Instructions for creating these types of applications can be found [here](https://boinc.berkeley.edu/trac/wiki/BasicApi) or [here](https://boinc.berkeley.edu/trac/wiki/VboxApps), and work just the same with `boinc-server-docker`. 

In this guide, however, we describe an easier way to run jobs which uses `boinc2docker`. This tool (which comes preinstalled with `boinc-server-docker`) lets you package your science applications inside Docker containers which are then delivered to your hosts. This makes your code automatically work on Linux, Windows, and Mac, and allows it to have arbitrary dependencies (e.g. Python, etc...) The trade-off is that it only works on 64-bit machines (most of BOINC anyway), requires users to have Virtualbox installed, and does not (currently) support GPUs. 

To begin, we give a brief introduction to running Docker containers in general. The syntax to run a Docker container is `docker run <image> <command>` where `<image>` is the name of the image and `<command>` is a normal Linux shell command to run inside the container. For example, the Docker Hub provides the image `python:alpine` which has Python installed (the "alpine" refers to the fact that the base OS for the Docker image is Alpine Linux, which is super small and makes the entire container be only ~25Mb). Thus you could execute a Python command in this container like, 

```bash
docker run python:alpine python -c "print('Hello BOINC')"
```
and it would print the string "Hello BOINC". 

Suppose you wanted to run this as a BOINC job. To do so, first get a shell inside your server with `docker-compose exec apache bash` and from the project directory run, 

```bash
root@boincserver:~/project$ bin/boinc2docker_create_work.py \
    python:alpine python -c "print('Hello BOINC')"
```

As you see, the script `bin/boinc2docker_create_work.py` takes the same arguments as `docker run` but instead of running the container, it creates a job on your server which runs the container on the volunteer's computer. 

If you now connect a client to your server, it will download and run this job, and you will see "Hello BOINC" in the log file which is returned to the server after the job is finished. 

Note that to run these types of Docker-based jobs, the client computer will need 64bit [Virtualbox](https://www.virtualbox.org/wiki/Downloads) installed and "virtualization" enabled in the BIOS. 

If your jobs have output files, `boinc2docker` provides a special folder for this, `/root/shared/results`; any files written to this directory are automatically tar'ed up and returned as a BOINC result file. For example, if you ran the job, 

```bash
root@boincserver:~/project# bin/boinc2docker_create_work.py \
    python:alpine python -c "open('/root/shared/results/hello.txt','w').write('Hello BOINC')"
```
which creates a file "hello.txt" with contents "Hello BOINC", your server will receive a result file from the client which is a tar containing this file. BOINC results are stored by `boinc-server-docker` in a volume mounted by default at `/results` in the Apache container. 

Of course, the `python:alpine` image here was just an example, any Docker image will work, including ones you create yourself. 

#### Running without `boinc2docker`

Finally, we note that, although by default the test server comes with `boinc2docker` pre-installed, it can also be removed. To do so, set the `TAG` variable to be empty,

```bash
TAG="" docker-compose up -d
```

If you do not specify it, the default tag is `TAG="-b2d"`, which launches the server with `boinc2docker` pre-installed. 


## Creating your own project

Now that you understand the mechanics of how to launch a test server and submit some jobs, lets look at how to actually create your real server. There are two templates for starting a project, 

* **example_project/with_b2d** - this has `boinc2docker` pre-installed, just like the test server 
* **example_project/without_b2d** - if you don't need `boinc2docker`, this image comes without it and is slightly smaller

The first step is to copy one of these two folders to a new folder, which for the purpose of this guide we will call `myproject/` (you can, and should, version control this folder so that you have your project's entire history saved, e.g. like [Cosmology@Home](https://github.com/marius311/cosmohome)). The folder structure will look like this, 

```
myproject/
    docker-compose.yml
    .env
    images/
        apache/
            Dockerfile
        mysql/
            Dockerfile
        makeproject/
            Dockerfile
```

The three `Dockerfile`'s will contain any modifications your project needs on top of the default `boinc-server-docker` images. The `docker-compose.yml` file specifies how these containers work together, and will likely not need any modifications from you. The `.env` file contains some customizable configuration options which you can change. 

### Building and running your server

The test server did not require us to build any Docker containers because these were pre-built, stored on the Docker Hub, and were downloaded to your machine when you executed the `docker-compose pull` command. The images which comprise your server, on the other hand, need to be built; the command to do so is simply `docker-compose build`. 

Afterwards, you can run a `docker-compose up -d` just as before to start the server. Of course, at this point you have made no modifications at all so the server is identical to the test server. We will discuss how to customize your server shortly. Note that you can combine the build and run commands into one with `docker-compose up -d --build`.

To stop your server, run `docker-compose down`. If you wish to reset your server entirely (i.e. to also delete the volumes housing your database and project folder), run `docker-compose down -v`. 

