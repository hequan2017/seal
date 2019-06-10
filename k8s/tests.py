
from kubernetes import client, config


def main():
    Token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tZGhobWMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOThkMDcwZWItODc1Yy0xMWU5LWE1MzgtMDAwYzI5N2I0ZmU3Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.XDFpez2E84R_zlopt_uEHPvVGUtSavypyix6UcYJO3J4imHdJy7MEkfV-wltBA1H8x0TT2AW64rLlXaRJ8OkFWJ0myedfKdjnf7i0oLQ8j-7lw6rT3A0e2pKmpnOaBQfgzRm83-t2I5MMp3Iu9VNUiAbqQpjql4AKwRuJEEGCs99tKStUxzIsJKusmUHh9KAK4BAxySn9h16T2URZ7czLP4mty2crYWNV4KwSwFPthGhFPsl8mnet_hiV5k4me5a8frmXytOy64MmGW8w3TBgiM-7hBYSxt84QGGnyi84LU0EFgtLwBWEOTZeUKKQ6IkoAprMmNcSxX8WUJFlx_uJg"
    APISERVER = 'https://192.168.100.111:6443'
    configuration = client.Configuration()
    configuration.host = APISERVER
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + Token}
    client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()