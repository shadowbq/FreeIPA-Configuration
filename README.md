# Test LDAP functionality using FreeIPA public server 

This uses the default always on demo server

UI - https://ipa.demo1.freeipa.org/ipa/ui/  

You can launch your own https://hub.docker.com/r/freeipa/freeipa-server/

* https://www.freeipa.org/page/Demo

## Dex

* https://github.com/mesosphere/dex/blob/v2.22.0-mesosphere/Documentation/connectors/ldap.md

## D2iQ Konvoy

* https://docs.d2iq.com/ksphere/konvoy/1.4/security/external-idps/howto-dex-ldap-connector/

## Connection 

```yaml
Host: ipa.demo1.freeipa.org
Port: 389
```

## Authentication

```yaml
Look DN: uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
Password: Secret123
# Authentication Method Simple
User DN Template: uid=%(username)s,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
```

Searching for a username using `uid`

![Searching for a username using `uid`](media/user-sn.png)

## Users

The FreeIPA domain is configured with the following users:

The password is **`Secret123`** for all of them

`admin`: The FreeIPA main administrator account, has all the privileges.  
`helpdesk`: A regular user with the helpdesk role allowing it to modify other users or change their group membership.  
`employee`: A regular user with no special privileges.  
`manager`: A regular user, set as manager of the employee user.  

**Note:** The `admin` does not have a `mail` ldap object. (This can cause issues if trying to use it as the the login/username object). All the others have a `mail` object.

|User login|	First name	|Last name	|Status	|UID	|Email address|
|---|---|---|---|---|---|
|admin||Administrator|Enabled|1162400000||
|employee|Test|Employee| Enabled|1162400009|employee@demo1.freeipa.org|
|helpdesk|Test|Helpdesk| Enabled|1162400004|helpdesk@demo1.freeipa.org|
|manager|Test|Manager| Enabled|1162400001|manager@demo1.freeipa.org|
|midpoint|midpoint|Medpoint_last_name| Enabled|1162400010|midpoint@demo1.freeipa.org|

### DC/OS User Template

DC/OS maps LDAP `uid` to DC/OS `username`

```yaml
User DN Template: uid=%(username)s,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
```

## Groups

To allow testing group-based authentication we created additional groups in addition to the default FreeIPA ones:

`employees`: contains users employee and manager.
`managers`: contains user manager.  

|Group name|	GID	|Description|
|---|---|---|
|admins|1162400000|Account administrators group|
|editors|1162400002|Limited admins who can edit other users|
|employees|1162400005|Test Employees|
|ipausers||Default group for all users|
|managers|1162400006|Test Managers|
|test|1162400011|test|
|trust admins||Trusts administrators group|

## Group Import

### DC/OS Group Template

DC/OS maps LDAP Group `cn` to DC/OS `groupname`

```yaml
Group Search Base: cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
Group Search Filter Template: (cn=%(groupname)s)
```

![Searching for a username using `cn`](media/group-cn.png)

## Docker and Container Issues

It is not tagging with version numbers (a major anti-pattern), it's only using latest.

* https://www.github.com/Tiboris/freeipa-container
* https://hub.docker.com/r/freeipa/freeipa-server/builds
* https://travis-ci.org/github/freeipa/freeipa-container

Similar RH OpenShift:  

RH Semi-Clone with proper tagging as noted in #https://github.com/freeipa/freeipa-container/issues/246  

* https://access.redhat.com/containers/?tab=tags#/registry.access.redhat.com/rhel7/ipa-server  
* https://access.redhat.com/containers/?tab=overview&get-method=unauthenticated#/registry.access.redhat.com/rhel7/ipa-server  
