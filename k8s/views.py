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
from k8s.k8sApi.core import K8sApi

logger = logging.getLogger('k8s')


class K8sPodListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('k8s.view_ecs',)
    template_name = 'k8s/k8s-pod-list.html'

    def get(self, request):
        ret = K8sApi().list_pod_for_all_namespaces(watch=False)
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"ip": i.status.pod_ip, "namespace": i.metadata.namespace}
        return render(request, "k8s/k8s-pod-list.html", {"data": data})
