# D2iQ DC/OS

## DC/OS User Template

Authentication Method Simple

DC/OS maps LDAP `uid` to DC/OS `username`

```yaml
User DN Template: uid=%(username)s,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
```

### Dex on D2IQ KSphere

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ldap-bind-password
  namespace: kubeaddons
type: Opaque
stringData:
  password: Secret123
---
apiVersion: dex.mesosphere.io/v1alpha1
kind: Connector
metadata:
  name: ldap
  namespace: kubeaddons
spec:
  enabled: true
  type: ldap
  displayName: LDAP Test
  ldap:
    host: ipa.demo1.freeipa.org:389
    insecureNoSSL: true
    bindDN: uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
    bindSecretRef:
      name: ldap-bind-password
    userSearch:
      baseDN: cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org
      filter: "(objectClass=person)"
      username: uid
      idAttr: uid
      emailAttr: mail
    groupSearch:
      baseDN: cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
      filter: "(objectClass=groupOfUniqueNames)"
      userAttr: DN
      groupAttr: uniqueMember
      nameAttr: ou
```

https://docs.d2iq.com/ksphere/konvoy/latest/security/external-idps/howto-dex-ldap-connector/

## DC/OS Group Template

DC/OS maps LDAP Group `cn` to DC/OS `groupname`

```yaml
Group Search Base: cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org
Group Search Filter Template: (cn=%(groupname)s)
```
