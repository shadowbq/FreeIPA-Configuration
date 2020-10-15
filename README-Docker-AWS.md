# FreeIPA Centos running on AWS instance with Docker

## Pre-reqs

1. Ubuntu 18.04 EC2 instance with internet access outbound.
2. Install `docker-ce` & setup on the ec2 host [install-docker-ce-ubuntu-1804](https://www.linode.com/docs/applications/containers/install-docker-ce-ubuntu-1804/)
3. Agree to use Image `freeipa/freeipa-server:centos-7-4.6.6`

## Create a AWS SG with the following

### Docker ports

Internal Ports

```
53/tcp, 80/tcp, 53/udp, 88/udp, 88/tcp, 389/tcp, 443/tcp, 123/udp, 464/tcp, 636/tcp, 464/udp
```

### AWS Security Group

Note: I'm not using ntp, dns, or kerbose outside the EC2 instance.

```
80	TCP	sg-037b0297bb8e183de	freeipa-sg
22	TCP	0.0.0.0/0	freeipa-sg
636	TCP	0.0.0.0/0	freeipa-sg
636	TCP	::/0	freeipa-sg
389	TCP	0.0.0.0/0	freeipa-sg
389	TCP	::/0	freeipa-sg
443	TCP	0.0.0.0/0	freeipa-sg
443	TCP	::/0	freeipa-sg
```

### Make the Data Warehouse

```
mkdir -p /opt/data/ipa-data
chmod a+w /opt/data/ipa-data
```

### Initialize the Server

Note: Im not mapping DNS(53) off the container.

`-h (Ensure you put the proper hostname for your instance)`

```shell
docker run --name freeipa-server-container -ti \
    -h  ec2-1-2-3-4.compute-1.amazonaws.com --read-only \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
    -v /opt/data/ipa-data:/data:Z \
    -p 443:443/tcp \
    -p 389:389/tcp \
    -p 636:636/tcp \
    -p 88:88/tcp \
    -p 88:88/udp \
    -p 464:464/tcp \
    -p 464:464/udp \
    -p 123:123/udp \
    --tmpfs /run --tmpfs /tmp \
    --sysctl net.ipv6.conf.all.disable_ipv6=0 \
    freeipa/freeipa-server:centos-7-4.6.6
```

Initial setup is interactive..

```
Server host name [ec2-1-2-3-4.compute-1.amazonaws.com]:

The domain name has been determined based on the host name.

Please confirm the domain name [compute-1.amazonaws.com]: example.test

The kerberos protocol requires a Realm name to be defined.
This is typically the domain name converted to uppercase.

Please provide a realm name [EXAMPLE.TEST]:
Certain directory server operations require an administrative user.
This user is referred to as the Directory Manager and has full access
to the Directory for system management tasks and will be added to the
instance of directory server created for IPA.
The password must be at least 8 characters long.

Directory Manager password:
Password (confirm):

The IPA server requires an administrative user, named 'admin'.
This user is a regular system account used for IPA server administration.

IPA admin password:
Password (confirm):


The IPA Master Server will be configured with:
Hostname:       ec2-1-2-3-4.compute-1.amazonaws.com
IP address(es): 172.17.0.2
Domain name:    example.test
Realm name:     EXAMPLE.TEST

Continue to configure the system with these values? [no]: yes

The following operations may take some minutes to complete.
Please wait until the prompt is returned.

Configuring NTP daemon (ntpd)
  [1/4]: stopping ntpd
  [2/4]: writing configuration
  [3/4]: configuring ntpd to start on boot
  [......]
  Removed symlink /etc/systemd/system/container-ipa.target.wants/ipa-server-configure-first.service.
  FreeIPA server configured.
```  

### Start the Server (subsequent times)

`docker start freeipa-server-container`



### Stop the Server

`docker stop freeipa-server-container`

```
## logs of a termination
Sending SIGTERM to remaining processes...
Sending SIGKILL to remaining processes...
Halting system.
Exiting container.
```

### Monitor the logs

```
$> docker logs -f freeipa-server-container
[...]
FreeIPA server is already configured, starting the services.
Thu Oct 15 16:04:08 UTC 2020 /usr/sbin/ipa-server-configure-first update-self-ip-address
FreeIPA server does not run DNS server, skipping update-self-ip-address.
FreeIPA server started.
```

