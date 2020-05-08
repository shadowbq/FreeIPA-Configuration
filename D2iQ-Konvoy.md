# D2iQ - Konvoy LDAP connection to FreeIPA/LDAP

## Summary 

You can easily hook Dex to provide ldap functionality to Konvoy. 

### *Dex*

`Dex` is deployed as an `addon` in Konvoy

* (private) https://github.com/mesosphere/dex/blob/v2.22.0-mesosphere/Documentation/connectors/ldap.md


Note:  You can **not** use the `./extras/kubernetes` folders for automation, because addons are fired after 
ansible's `STAGE [Deploying Additional Kubernetes Resources]`

### *Tutorial*

There is a somewhat incomplete tutorial using a different open ldap demo server.

* https://docs.d2iq.com/ksphere/konvoy/1.4/security/external-idps/howto-dex-ldap-connector/

There are other tutorials using OAuth (watch out for the age of the konvoy references)

* https://github.com/mesosphere/konvoy-training#appendix-1-setting-up-an-external-identity-provider

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

### *Authenticated for `kubectl` Token use*

Requesting Configurations for using ldap `admin` in `kubectl`.

![Token Request](media/TokenRequest.png)

Setting `kubectl` config using ldap `admin` .

![kubectl config set](media/kubectl-config-set.png)

Using `admin-kubernetes-cluster` context in `kubectl` config using ldap `admin`.

![kubectl use](media/kubectl-config-use.png)

### *Authenticated for Opsportal use*

Login using the LDAP TEST.

![Select Portal](media/LDAP-Option.png)

Fully authenticated and authorized using ldap `admin` in `kubectl`.

![Ops Login](media/PerfectOpsPortal-1.5.png)

### *Authentication using the `konvoy-async-auth` plugin*

When enabled the plugin initiates authentication sessions and stores identity tokens automatically.

As an example, Im going to want to go to `/token/plugin` in 1.5.x konvoy.

![Konvoy Async Auth Plugin](media/konvoy-async-auth.png)

hxxps://some-elb-dns-instance.us-east-1.elb.amazonaws.com/token/plugin

Konvoy kubectl credentials plugin

This document describes the process of configuring kubectl to use the Konvoy credentials plugin. This credentials plugin makes it easy to use external identity provider accounts with the kubernetes API. When enabled the plugin initiates authentication sessions and stores identity tokens automatically.

* Generate a kubeconfig
* Configure Access to Multiple Clusters
* Build kubeconfig with kubectl
* Copy cluster CA certificate
* Download and Install Konvoy credentials plugin
* Configure kubectl to use the Plugin
* Create a cluster configuration
* Create kubeconfig user Profile
* Create the context
    
If this is the first time you've attempted to authenticate using the plugin, a browser window opens to the Konvoy authentication page. After successful authentication, you should see a pod listing in your terminal. The plugin stores your identity token for subsequent requests. After your identity token expires, by **default 24 hours**, the plugin directs you to the Konvoy authentication page where you can re-authenticate.

### *Set additional RBACS*

Grant the user `opsportal-admin` role

```
$ kubectl describe clusterroles opsportal-admin
describe clusterroles opsportal-admin
Name:         opsportal-admin
Labels:       app.kubernetes.io/instance=opsportal-kubeaddons
              app.kubernetes.io/managed-by=Tiller
              app.kubernetes.io/version=1.0.0
Annotations:  <none>
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
             [/ops/portal/*]    []              [delete]
             [/ops/portal]      []              [delete]
             [/ops/portal/*]    []              [get]
             [/ops/portal]      []              [get]
             [/ops/portal/*]    []              [head]
             [/ops/portal]      []              [head]
             [/ops/portal/*]    []              [post]
             [/ops/portal]      []              [post]
             [/ops/portal/*]    []              [put]
             [/ops/portal]      []              [put]
```             

* More RBAC in the Portal: https://docs.d2iq.com/ksphere/konvoy/1.5.0-beta/security/external-idps/rbac/

### *Authenticated into Kommander with Federation*

(Fix this) Fully authenticated and authorized using "admin" in "opsportal".

![Wrong Password](media/PerfectOpsPortal-1.5.png)

## Refresh Credentials

When the token expires, it is necessary to repeat the above process to obtain a fresh token. When refreshing a token, only the `kubectl config set-credentials ... --token=ABCCC` command needs to be executed with the new token.

Also see: ***Authentication using the `konvoy-async-auth` plugin***

## Tunables

### Expiry of Dex Tokens

Identity token issued by Dex expire after **default 24 hours**.

You can change the Dex expiry by injecting into the helm chart values a new config option

![dex extended addon expiry](media/dex-addon-chart-modify.png)

## Troubleshooting Konvoy

### *Find the `Dex` pods*

Use the `kubeaddons` namespace when looking for them:

```shell
$ kubectl get pods --namespace kubeaddons |grep ^dex
dex-k8s-authenticator-kubeaddons-57bcc8f449-xvr7n                 1/1     Running     2          3h2m
dex-kubeaddons-dd869fc8f-j4xcf                                    1/1     Running     0          2m42s
dex-kubeaddons-dex-controller-6b6c9fbd7f-sscb7                    2/2     Running     0          3h39m
```

### *Issues with Binding* 

There are two or three issues covered in here:

https://docs.d2iq.com/ksphere/konvoy/1.4/security/external-idps/howto-dex-ldap-connector/

### *`Not Authorized` is not the same as `Not Authenticated!`*

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

### *`Not Authenticated` but binding works*

This is very simple, you are use the wrong password for the current user.

![Wrong Password](media/konvoy-wrong-password.png)


## Bearer Tokens 

The Token installation looks like this:
```shell
$ kubectl config set-credentials cranky_hypatia-kubernetes-cluster \
    --token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ4NjdkMmE3YjhjYzA2N2I4N2JhNGM5NGFjYjllY2IyOTFkNDM4ZTUifQ.eyJpc3MiOiJodHRwczovL2E3ZTIwZmMwMGU2MzE0MTE0YjY1YmQ4ZWI2NWNkY2FmLTY3Nzk3NjY3LnVzLWVhc3QtMS5lbGIuYW1hem9uYXdzLmNvbS9kZXgiLCJzdWIiOiJDaVF5WW1ObE16VmxZUzFtWlRNNUxUUXpZMll0T1dVNFppMDBaVFF5TURjeVlXVTVOVEVTQld4dlkyRnMiLCJhdWQiOiJrdWJlLWFwaXNlcnZlciIsImV4cCI6MTU4OTEzMDg2OCwiaWF0IjoxNTg4OTU4MDY4LCJhdF9oYXNoIjoiaDE2RWZEd1JNN05XM0czTnZxTlBhUSIsImVtYWlsIjoiY3Jhbmt5X2h5cGF0aWEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6ImNyYW5reV9oeXBhdGlhIn0.qSJNAxH5xBLfd2ycA7356NpMtXcuNUhtomDpd5WTDb41VGdjfwkSbSMLe1OpBB3eu0iiKoafrUaJzHM78cUEnuOxJlaQtrB-PhOcg2eQPW4PFOda2IQYUQCQPuW5Gx6pBe3yldx5thFcaP7bYIbNDbRUAJi6Tz5stLhYk9ISdsqhpSOWiQK5gboGGC-rLTVQ3KidMup4g3kCdcImt5BdUD42jj4J5BbwSPk9m7OayWhpbjY2lC9OR-UW14sfm1xQuKDOGxpxxwuHuth2sIkYGxyuN0LAKYLCBtw9OEvFnwJXI3wdi0ElV8btt-5t93zXw_aFNm60-SEKFeiTE1liIw
```

Taking the Token out: (make note of the "." dots)

```
eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ4NjdkMmE3YjhjYzA2N2I4N2JhNGM5NGFjYjllY2IyOTFkNDM4ZTUifQ.eyJpc3MiOiJodHRwczovL2E3ZTIwZmMwMGU2MzE0MTE0YjY1YmQ4ZWI2NWNkY2FmLTY3Nzk3NjY3LnVzLWVhc3QtMS5lbGIuYW1hem9uYXdzLmNvbS9kZXgiLCJzdWIiOiJDaVF5WW1ObE16VmxZUzFtWlRNNUxUUXpZMll0T1dVNFppMDBaVFF5TURjeVlXVTVOVEVTQld4dlkyRnMiLCJhdWQiOiJrdWJlLWFwaXNlcnZlciIsImV4cCI6MTU4OTEzMDg2OCwiaWF0IjoxNTg4OTU4MDY4LCJhdF9oYXNoIjoiaDE2RWZEd1JNN05XM0czTnZxTlBhUSIsImVtYWlsIjoiY3Jhbmt5X2h5cGF0aWEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6ImNyYW5reV9oeXBhdGlhIn0.qSJNAxH5xBLfd2ycA7356NpMtXcuNUhtomDpd5WTDb41VGdjfwkSbSMLe1OpBB3eu0iiKoafrUaJzHM78cUEnuOxJlaQtrB-PhOcg2eQPW4PFOda2IQYUQCQPuW5Gx6pBe3yldx5thFcaP7bYIbNDbRUAJi6Tz5stLhYk9ISdsqhpSOWiQK5gboGGC-rLTVQ3KidMup4g3kCdcImt5BdUD42jj4J5BbwSPk9m7OayWhpbjY2lC9OR-UW14sfm1xQuKDOGxpxxwuHuth2sIkYGxyuN0LAKYLCBtw9OEvFnwJXI3wdi0ElV8btt-5t93zXw_aFNm60-SEKFeiTE1liIw
```

### That ID Token is a JWT with three base64'd fields separated by dots. 

(Base64 decode each section without including the dots) 

* The first is a header, 
* the second is a payload, 
* the third is a signature of the first two fields. 

1st Group - *Header*

```json
{"alg":"RS256","kid":"d867d2a7b8cc067b87ba4c94acb9ecb291d438e5"}
```

2nd Group - *Payload*

The payload contains:  
`iat` which is the time of issuance - EPOCH **Friday, May 8, 2020 5:14:28 PM**  
`exp` which is *48h* after the `iat` - EPOCH of **Sunday, May 10, 2020 5:14:28 PM**  

Note: This is *48h* because we've edited the dex addon controller in the section **Expiry of Dex Tokens** to change to *48h* from the default of *24h*

```json
{
  "iss": "https://a7e20fc00e6314114b65bd8eb65cdcaf-67797667.us-east-1.elb.amazonaws.com/dex",
  "sub": "CiQyYmNlMzVlYS1mZTM5LTQzY2YtOWU4Zi00ZTQyMDcyYWU5NTESBWxvY2Fs",
  "aud": "kube-apiserver",
  "exp": 1589130868,
  "iat": 1588958068,
  "at_hash": "h16EfDwRM7NW3G3NvqNPaQ",
  "email": "cranky_hypatia",
  "email_verified": true,
  "name": "cranky_hypatia"
}
```

3rd Group - *Signature*

```qSJNAxH5xBLfd2ycA7356NpMtXcuNUhtomDpd5WTDb41VGdjfwkSbSMLe1OpBB3eu0iiKoafrUaJzHM78cUEnuOxJlaQtrB-PhOcg2eQPW4PFOda2IQYUQCQPuW5Gx6pBe3yldx5thFcaP7bYIbNDbRUAJi6Tz5stLhYk9ISdsqhpSOWiQK5gboGGC-rLTVQ3KidMup4g3kCdcImt5BdUD42jj4J5BbwSPk9m7OayWhpbjY2lC9OR-UW14sfm1xQuKDOGxpxxwuHuth2sIkYGxyuN0LAKYLCBtw9OEvFnwJXI3wdi0ElV8btt-5t93zXw_aFNm60-SEKFeiTE1liIw```

An Additional Example of the 2nd Group with an LDAP User:

Note: The lack of username, as the ldap user is supposed to login in with an email address, but I've configure it to use the `uid` as FreeIPA lacks an email address for *"admin"*.

```json
{
  "iss": "https://a7e20fc00e6314114b65bd8eb65cdcaf-67797667.us-east-1.elb.amazonaws.com/dex",
  "sub": "CgVhZG1pbhITZGV4LWNvbnRyb2xsZXItbGRhcA",
  "aud": "kube-apiserver",
  "exp": 1589133095,
  "iat": 1588960295,
  "at_hash": "QXsmTOQ2EAszrRbc9j5Maw",
  "email": "admin",
  "email_verified": true
}
```
