from kubernetes import client, config
from seal import settings
import urllib3


def K8sApi():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    configuration = client.Configuration()
    configuration.host = getattr(settings, 'APISERVER')
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + getattr(settings, 'Token'), }
    client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()

    return v1
