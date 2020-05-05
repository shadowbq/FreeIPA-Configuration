# D2iQ DC/OS

## DC/OS User Template

Authentication Method Simple

DC/OS maps LDAP `uid` to DC/OS `username`

```yaml
User DN Template: uid=%(username)s,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
```

## DC/OS Group Template

DC/OS maps LDAP Group `cn` to DC/OS `groupname`

```yaml
Group Search Base: cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
Group Search Filter Template: (cn=%(groupname)s)
```
