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
from assets.form import EcsForm
from assets.serializers import EcsSerializer
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger('assets')


## 关于 cbv 的 文档 http://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/
class EcsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Ecs 创建
    """
    permission_required = ('assets.add_ecs',)
    model = Ecs
    form_class = EcsForm
    template_name = 'assets/ecs-create.html'
    success_url = reverse_lazy('assets:ecs-list')

    def get_context_data(self, **kwargs):
        context = {}
        if '__next__' in self.request.POST:  # 为了获取 点击本页之前的 浏览网页
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                logger.error(e)
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.request.POST['__next__']

    def form_valid(self, form):  #  保存结果 可以进行 手动 修改 再保存
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class EcsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('assets.view_ecs',)
    template_name = 'assets/ecs-list.html'
    model = Ecs
    queryset = Ecs.objects.get_queryset().order_by('-id')

    @get_list  ## 处理查询
    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        ecs_list = p.page(page)

        context = {
            "ecs_list": ecs_list,
            'ecs_count': self.queryset.count() if self.queryset != '' else 0,
            "filter_dict": self.filter_dict  # 把查询条件返回给前端
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)


class EcsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Ecs 更新
    """
    permission_required = ('assets.change_ecs',)
    model = Ecs
    form_class = EcsForm
    template_name = 'assets/ecs-create.html'
    success_url = reverse_lazy('assets:ecs-list')

    def get_context_data(self, **kwargs):
        context = {}
        if '__next__' in self.request.POST:  # 为了获取 点击本页之前的 浏览网页
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                logger.error(e)
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.request.POST['__next__']


class EcsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('assets.view_ecs',)
    model = Ecs
    form_class = EcsForm
    template_name = 'assets/ecs-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        context = {
            "ecs": self.model.objects.get(id=pk),
            "nid": pk
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class EcsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Ecs 删除
    """
    permission_required = ('asset.delete_ecs',)
    model = Ecs

    def post(self, request):
        ret = {'status': True, 'error': None, }
        nid = self.request.POST.get('nid', None)
        self.model.objects.get(id=nid).delete()
        return HttpResponse(json.dumps(ret))


# Ecs Api           drf 中文文档   http://drf.jiuyou.info/#/drf/requests
class ApiEcsList(generics.ListCreateAPIView):
    queryset = Ecs.objects.get_queryset().order_by('id')
    serializer_class = EcsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('id', 'hostname','type','instance_id')
    search_fields = ('id', 'hostname',)
    permission_classes = (permissions.DjangoModelPermissions,)  # 继承 django的权限


class ApiEcsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ecs.objects.get_queryset().order_by('id')
    serializer_class = EcsSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

