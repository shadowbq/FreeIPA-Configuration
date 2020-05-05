# D2iQ - Konvoy LDAP connection to FreeIPA/LDAP

## Summary 

You can easily hook Dex to provide ldap functionality to Konvoy. 

### Dex

`Dex` is deployed as an `addon` in Konvoy

* https://github.com/mesosphere/dex/blob/v2.22.0-mesosphere/Documentation/connectors/ldap.md

Note:  You can **not** use the `./extras/kubernetes` folders for automation, because addons are fired after 
ansible's `STAGE [Deploying Additional Kubernetes Resources]`

### Tutorial

There is a somewhat incomplete tutorial using a different open ldap demo server.

* https://docs.d2iq.com/ksphere/konvoy/1.4/security/external-idps/howto-dex-ldap-connector/

## Deploying Manifest to Konvoy

The `manifests/ldap/` define some basic configuration for the ldap binding.

```shell
$ kubectl apply -f manifests/
secret/ldap-password configured
connector.dex.mesosphere.io/ldap unchanged
clusterrolebinding.rbac.authorization.k8s.io/cluster-admin-ldapadmin unchanged
clusterrole.rbac.authorization.k8s.io/prom-admin unchanged
clusterrolebinding.rbac.authorization.k8s.io/prom-rbac created
```


## D2iQ Ksphere Konvoy 1.5.x using correctly configured LDAP 

### Authenticated for `kubectl` Token use

Requesting Configurations for using ldap `admin` in `kubectl`.

![Token Request](media/TokenRequest.png)

Setting `kubectl` config using ldap `admin` .

![kubectl config set](media/kubectl-config-set.png)

Using `admin-kubernetes-cluster` context in `kubectl` config using ldap `admin`.

![kubectl use](media/kubectl-config-use.png)

### Authenticated for Opsportal use

Login using the LDAP TEST.

![Select Portal](media/LDAP-Option.png)

Fully authenticated and authorized using ldap `admin` in `kubectl`.

![Ops Login](media/PerfectOpsPortal-1.5.png)

### Set additional RBACS

(Need more RBAC information here)

### Authenticated into Kommander with Federation

(Fix this) Fully authenticated and authorized using "admin" in "opsportal".

![Wrong Password](media/PerfectOpsPortal-1.5.png)

## Troubleshooting Konvoy

### Find the `Dex` pods

Use the `kubeaddons` namespace when looking for them:

```shell
$ kubectl get pods --namespace kubeaddons |grep ^dex
dex-k8s-authenticator-kubeaddons-57bcc8f449-xvr7n                 1/1     Running     2          3h2m
dex-kubeaddons-dd869fc8f-j4xcf                                    1/1     Running     0          2m42s
dex-kubeaddons-dex-controller-6b6c9fbd7f-sscb7                    2/2     Running     0          3h39m
```

### Issues with Binding 

There are two or three issues covered in here:

https://docs.d2iq.com/ksphere/konvoy/1.4/security/external-idps/howto-dex-ldap-connector/

### `Not Authorized` is not the same as `Not Authenticated!`

This is actually not an error, but a permissions issue.

`admin` Did actually login! **You need to fix RBAC.**

```
$ kubectl logs -f dex-kubeaddons-dd869fc8f-j4xcf -n kubeaddons
time="2020-05-04T20:19:36Z" level=info msg="performing ldap search cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org sub (&(objectClass=person)(uid=admin))"
time="2020-05-04T20:19:36Z" level=info msg="username \"admin\" mapped to entry uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org"
time="2020-05-04T20:19:36Z" level=info msg="performing ldap search cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org sub (&(objectClass=groupofnames)(uniqueMember=uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org))"
time="2020-05-04T20:19:36Z" level=error msg="ldap: groups search with filter \"(&(objectClass=groupofnames)(uniqueMember=uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org))\" returned no groups"
time="2020-05-04T20:19:36Z" level=info msg="login successful: connector \"dex-controller-ldap\", username=\"\", preferred_username=\"\", email=\"admin\", groups=[]"
```

![Not Authorized](media/Not-Authorized.png)

### `Not Authenticated` but binding works

This is very simple, you are use the wrong password for the current user.

![Wrong Password](media/konvoy-wrong-password.png)

