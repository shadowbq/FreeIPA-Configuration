# Using OpenLDAP 

We will assume no connection to *demo1.freeipa.org*. Thus we will manually connect and authenticate each time without reling on `/etc/openldap/ldap.conf`. 

## Search for "employee" with `ldapsearch`

```shell
$ ldapsearch -x -D "uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org" -W -b "dc=demo1,dc=freeipa,dc=org" -h ipa.demo1.freeipa.org -s sub "(&(objectclass=*)(uid=employee))"
Enter LDAP Password:
```

Will find "employee" by:

* -x - simple authentication
* -D - Use bind user "search-user"
* -W - Prompt for password
* -b - The search base
* -h - Host name 
* -s - Search scope 

Ommitted but you could include: 

* -H - URL of LDAP server. Non-SSL in this case; use "ldaps://" for SSL

```ini
# extended LDIF
#
# LDAPv3
# base <dc=demo1,dc=freeipa,dc=org> with scope subtree
# filter: (&(objectclass=*)(uid=employee))
# requesting: ALL
#

# employee, users, compat, demo1.freeipa.org
dn: uid=employee,cn=users,cn=compat,dc=demo1,dc=freeipa,dc=org
objectClass: posixAccount
objectClass: top
gecos: Test Employee
cn: Test Employee
uidNumber: 1162400003
gidNumber: 1162400003
loginShell: /bin/sh
homeDirectory: /home/employee
uid: employee

# employee, users, compat, demo1.freeipa.org
dn: uid=employee,cn=users,cn=compat,dc=demo1,dc=freeipa,dc=org
objectClass: posixAccount
objectClass: ipaOverrideTarget
objectClass: top
gecos: Test Employee
cn: Test Employee
uidNumber: 1162400003
gidNumber: 1162400003
loginShell: /bin/sh
homeDirectory: /home/employee
ipaAnchorUUID:: OklQQTpkZW1vMS5mcmVlaXBhLm9yZzoxYzRmYjEwOC05MGQ4LTExZTgtYjUxYi
 0wNjI4NTA4YTE3NGU=
uid: employee

# employee, users, accounts, demo1.freeipa.org
dn: uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
givenName: Test
sn: Employee
uid: employee
cn: Test Employee
displayName: Test Employee
initials: TE
gecos: Test Employee
krbPrincipalName: employee@DEMO1.FREEIPA.ORG
manager: uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
objectClass: top
objectClass: person
objectClass: organizationalperson
objectClass: inetorgperson
objectClass: inetuser
objectClass: posixaccount
objectClass: krbprincipalaux
objectClass: krbticketpolicyaux
objectClass: ipaobject
objectClass: ipasshuser
objectClass: ipaSshGroupOfPubKeys
objectClass: mepOriginEntry
objectClass: ipantuserattrs
loginShell: /bin/sh
homeDirectory: /home/employee
mail: employee@demo1.freeipa.org
krbCanonicalName: employee@DEMO1.FREEIPA.ORG
ipaUniqueID: 1c4fb108-90d8-11e8-b51b-0628508a174e
uidNumber: 1162400003
gidNumber: 1162400003
krbLastPwdChange: 20190125151611Z
krbExtraData:: AAI7KEtca2FkbWluZEBERU1PMS5GUkVFSVBBLk9SRwA=
mepManagedEntry: cn=employee,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
memberOf: cn=ipausers,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
memberOf: cn=employees,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
krbTicketFlags: 128
krbLoginFailedCount: 0
ipaNTSecurityIdentifier: S-1-5-21-3656337171-3937262974-1104883008-1003

# search result
search: 2
result: 0 Success

# numResponses: 4
# numEntries: 3
```

Reference:

https://www.thegeekstuff.com/2015/02/openldap-add-users-groups/
