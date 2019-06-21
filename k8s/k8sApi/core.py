from kubernetes import client, config
from seal import settings
import urllib3
from kubernetes.stream import stream


class K8sApi(object):

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_client(self):
        baseurl = getattr(settings, 'APISERVER')
        token = getattr(settings, 'Token')
        aConfiguration = client.Configuration()
        aConfiguration.host = baseurl
        aConfiguration.verify_ssl = False
        aConfiguration.api_key = {"authorization": "Bearer " + token}
        aApiClient = client.ApiClient(aConfiguration)
        v1 = client.CoreV1Api(aApiClient)

        return v1

    def get_node_list(self):
        client_v1 = self.get_client()
        ret = client_v1.list_node()
        return ret

    def get_service_list(self):
        client_v1 = self.get_client()
        ret = client_v1.list_service_for_all_namespaces(watch=False)
        return ret

    def get_pod_list(self):
        client_v1 = self.get_client()
        ret_pod = client_v1.list_pod_for_all_namespaces(watch=False)
        return ret_pod

    def get_pod_detail(self, name, namespace):
        client_v1 = self.get_client()
        ret_pod = client_v1.read_namespaced_pod(name, namespace)
        return ret_pod

    def terminal_start(self, namespace, pod_name, container):
        command = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
            '&& ([ -x /usr/bin/script ] '
            '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
            '|| exec /bin/sh']
        client_v1 = self.get_client()
        container_stream = stream(
            client_v1.connect_get_namespaced_pod_exec,
            name=pod_name,
            namespace=namespace,
            container=container,
            command=command,
            stderr=True, stdin=True,
            stdout=True, tty=True,
            _preload_content=False
        )

        return container_stream

