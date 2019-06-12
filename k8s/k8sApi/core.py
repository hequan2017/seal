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

    def get_namespace_list(self):
        client_v1 = self.get_client()
        ret_namespace = client_v1.list_namespace()
        return ret_namespace

    # def test_pod_connect(self, podname, namespace, command, container=None):
    #     client_v1 = self.get_client()
    #     if stream(client_v1.connect_get_namespaced_pod_exec, podname, namespace, command=command,
    #               container=container,
    #               stderr=True, stdin=False,
    #               stdout=True, tty=False):
    #         return True
    #     else:
    #         return False
    #
    # def get_pod_exec(self, podname, namespace, command, container=None):
    #     client_v1 = self.get_client()
    #     if container:
    #         rest = stream(client_v1.connect_get_namespaced_pod_exec, podname, namespace, command=command,
    #                       container=container,
    #                       stderr=True, stdin=False,
    #                       stdout=True, tty=False)
    #     else:
    #         rest = stream(client_v1.connect_get_namespaced_pod_exec, podname, namespace, command=command,
    #                       stderr=True, stdin=False,
    #                       stdout=True, tty=False)
    #     return rest
