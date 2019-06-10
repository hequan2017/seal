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


class K8sPodListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        obj = K8sApi()
        ret = obj.get_podlist()
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"ip": i.status.pod_ip, "namespace": i.metadata.namespace}
        return render(request, "k8s/k8s-pod-list.html", {"data": data})


class K8sPodWebssh(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)

    def get(self, request):
        name = self.request.GET.get("name")
        namespace = self.request.GET.get("namespace")
        return render(request, "k8s/k8s-pod-webssh.html",{"name":name,"namespace":namespace})

