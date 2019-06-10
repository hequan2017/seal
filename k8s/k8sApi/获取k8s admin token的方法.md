
## 1.先创建

```
vim k8s-admin.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dashboard-admin
  namespace: kube-system
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: dashboard-admin
subjects:
  - kind: ServiceAccount
    name: dashboard-admin
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io

kubectl apply -f k8s-admin.yaml
```
## 2.获取name
```
kubectl get secret -n kube-system
NAME                                             TYPE                                  DATA   AGE
dashboard-admin-token-dhhmc                      kubernetes.io/service-account-token   3      69s
```

## 3.查询token
```
[root@k8s-master ~]#  kubectl describe secret dashboard-admin-token-dhhmc   -n kube-system
Name:         dashboard-admin-token-dhhmc
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: dashboard-admin
              kubernetes.io/service-account.uid: 98d070eb-875c-11e9-a538-000c297b4fe7


Type:  kubernetes.io/service-account-token


Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tZGhobWMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOThkMDcwZWItODc1Yy0xMWU5LWE1MzgtMDAwYzI5N2I0ZmU3Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.XDFpez2E84R_zlopt_uEHPvVGUtSavypyix6UcYJO3J4imHdJy7MEkfV-wltBA1H8x0TT2AW64rLlXaRJ8OkFWJ0myedfKdjnf7i0oLQ8j-7lw6rT3A0e2pKmpnOaBQfgzRm83-t2I5MMp3Iu9VNUiAbqQpjql4AKwRuJEEGCs99tKStUxzIsJKusmUHh9KAK4BAxySn9h16T2URZ7czLP4mty2crYWNV4KwSwFPthGhFPsl8mnet_hiV5k4me5a8frmXytOy64MmGW8w3TBgiM-7hBYSxt84QGGnyi84LU0EFgtLwBWEOTZeUKKQ6IkoAprMmNcSxX8WUJFlx_uJg
```