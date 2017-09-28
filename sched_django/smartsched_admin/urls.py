from django.conf.urls import url

from .views import *
from django.shortcuts import redirect
from django.contrib import admin

urlpatterns = [
    url(r'^$', lambda _: redirect('admin:index'), name='index'),
    url(r'load_cloud_conf/?$', load_cloud_conf, name='load_cloud_conf'),
    url(r'drop_cloud_conf/?$', drop_cloud_conf, name='drop_cloud_conf'),
    url(r'get_host_info/?$', get_host_info, name='get_host_info'),
    url(r'get_cluster_info/?$', get_cluster_info, name='get_cluster_info'),
    url(r'get_vm_info/?$', get_vm_info, name='get_vm_info'),
    url(r'get_host_metrics/?$', get_host_metrics, name='get_host_metrics'),
    url(r'get_vm_metrics/?$', get_vm_metrics, name='get_vm_metrics'),
]

admin.site.site_header = 'SmartScheduler administration'
admin.site.site_title = 'SmartScheduler administration'
