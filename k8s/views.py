import logging
import json
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from pure_pagination import PageNotAnInteger
from pure_pagination import Paginator
from django.shortcuts import render, HttpResponse
from system.decorator.get_list import get_list
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView
from assets.models import Ecs
from seal import settings
from k8s.k8sApi.core import K8sApi

logger = logging.getLogger('k8s')


class K8sNodeListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        obj = K8sApi()
        ret = obj.get_node_list()
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"name": i.metadata.name,
                                     "status": i.status.conditions[-1].type if i.status.conditions[ -1].status == "True" else "NotReady",
                                     "ip": i.status.addresses[0].address,
                                     "kubelet_version": i.status.node_info.kubelet_version,
                                     "os_image": i.status.node_info.os_image,
                                     }
        return render(request, "k8s/k8s-node-list.html", {"data": data})


class K8sServiceListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        obj = K8sApi()
        ret = obj.get_service_list()
        data = {}
        for i in ret.items:
            print(i)
            ports = []
            for j in i.spec.ports:
                ports.append(f"{j.target_port}/{j.port}/{j.node_port}")
            data[i.metadata.name] = {"name": i.metadata.name, "cluster_ip": i.spec.cluster_ip, "type": i.spec.type,
                                     "external_i_ps": i.spec.external_i_ps,
                                     "port": ports}
        return render(request, "k8s/k8s-service-list.html", {"data": data})


class K8sPodListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        obj = K8sApi()
        ret = obj.get_pod_list()
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"ip": i.status.pod_ip, "namespace": i.metadata.namespace}
        return render(request, "k8s/k8s-pod-list.html", {"data": data})


class K8sPodWebssh(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        name = self.request.GET.get("name")
        namespace = self.request.GET.get("namespace")
        return render(request, "k8s/k8s-pod-webssh.html", {"name": name, "namespace": namespace})


class K8sPodDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        name = self.request.GET.get("name")
        namespace = self.request.GET.get("namespace")
        obj = K8sApi()
        data = obj.get_pod_detail(name, namespace)
        return render(request, "k8s/k8s-pod-detail.html", {"name": name, "namespace": namespace, "data": data})
