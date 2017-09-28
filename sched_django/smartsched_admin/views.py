from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from smartsched import common
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.contrib import messages
from django.template.loader import render_to_string
from django.template import RequestContext
import ast
import time
from django.conf import settings

def response_with_messages(msg, data, request):
     response = {
                'msg': render_to_string('admin/includes/messages.html', {}, request),
                'data': data
            }
     return HttpResponse(json.dumps(response), content_type="application/json")

def load_new_cloud_conf():
    cloud = common.get_cloud_handler()
    clusters = cloud.get_clusters_repr()
    for cluster in clusters:
        cluster_record = Cluster(
            cluster_id=cluster['id'], cluster_name=cluster['name'])
        cluster_record.save()

    hosts = cloud.get_hosts_repr()

    for host in hosts:
        host_record = Host(host_id=host['id'],
                           cpu=host['usage_cpu']['max'],
                           ram=host['usage_mem']['max'],
                           cluster=host['cluster_id']
                           )
        host_record.save()

    vms = cloud.get_vms_repr(vmStateFilter=3)
    for vm in vms:
        vm_record = VM(vm_id=vm['id'],
                       cpu=vm['cpu_req'],
                       ram=vm['mem_req'],
                       host=Host.objects.get(host_id=vm['hid'])
                       )
        vm_record.save()


def get_cloud_conf_changes():
    cloud = common.get_cloud_handler()
    result = {"clusters":{}, "hosts":{}, "vms":{}}
    hasChanges = False

    clusters = cloud.get_clusters_repr()
    clusters_db = Cluster.objects.all()

    for cluster in clusters:
        found_match = False
        for cluster_db in clusters_db:
            if cluster["id"] == cluster_db.cluster_id:
                found_match = True
                if cluster["name"] != cluster_db.cluster_name:
                    hasChanges = True
                    result["clusters"][str(cluster["id"])] = {"cluster_id": cluster['id'], "cluster_name": cluster['name'], "old_cluster_name": cluster_db.cluster_name}
        if not found_match:
            hasChanges = True
            result["clusters"][str(cluster["id"])] = {"cluster_id": cluster['id'], "cluster_name": cluster['name'], "old_cluster_name": "-"}

    hosts = cloud.get_hosts_repr()
    hosts_db = Host.objects.all()

    for host in hosts:
        found_match = False
        for host_db in hosts_db:
            if host["id"] == host_db.host_id:
                found_match = True
                if host_db.cpu != host['usage_cpu']['max'] or host_db.ram != host['usage_mem']['max'] or host_db.cluster != host['cluster_id']:
                    hasChanges = True
                    result["hosts"][host["id"]] = {'host_id': host['id'], 'cpu': host['usage_cpu']['max'], 'ram': host['usage_mem']['max'], 'cluster_id': host['cluster_id'],
                                                                                'old_cpu': host_db.cpu, 'old_ram': host_db.ram, 'old_cluster_id': host_db.cluster}
        if not found_match:
            hasChanges = True
            result["hosts"][host["id"]] = {'host_id': host['id'], 'cpu': host['usage_cpu']['max'], 'ram': host['usage_mem']['max'], 'cluster_id': host['cluster_id'],
                                                                        'old_cpu': "-", 'old_ram': "-", 'old_cluster_id': "-"}


    vms = cloud.get_vms_repr(vmStateFilter=3)
    vms_db = VM.objects.all().prefetch_related('host')

    for vm in vms:
        found_match = False
        for vm_db in vms_db:
            if vm['id'] == vm_db.vm_id:
                found_match = True
                if vm_db.cpu != vm['cpu_req'] or vm_db.ram != vm['mem_req'] or vm_db.host.host_id != vm['hid']:
                    hasChanges = True
                    result["vms"][vm["id"]] = {'vm_id': vm['id'], 'cpu': vm['cpu_req'], 'ram': vm['mem_req'], 'host_id': vm['hid'],
                                                                                        'old_cpu': vm_db.cpu, 'old_ram': vm_db.ram, 'old_host_id': vm_db.host.host_id}
        if not found_match:
            hasChanges = True
            result["vms"][vm["id"]] = {'vm_id': vm['id'], 'cpu': vm['cpu_req'], 'ram': vm['mem_req'], 'host_id': vm['hid'],
                                                                                    'old_cpu': "-", 'old_ram': "-", 'old_host_id': "-"}

    result['has'] = hasChanges

    return result

def update_cloud_conf(data):
    data = ast.literal_eval(data)
    for cluster_id, cluster in data['clusters'].items():
        try:
            cluster_record = Cluster.objects.get(cluster_id=cluster['cluster_id'])
            cluster_record.cluster_name = cluster['cluster_name']
        except Cluster.DoesNotExist:
            cluster_record = Cluster(cluster_id=cluster['cluster_id'], cluster_name=cluster['cluster_name'])

        cluster_record.save()

    for host_id, host in data['hosts'].items():
        try:
            host_record = Host.objects.get(host_id=host['host_id'])
            host_record.cpu = host["cpu"]
            host_record.ram = host["ram"]
            host_record.cluster = host["cluster_id"]
        except Host.DoesNotExist:
            host_record = Host(host_id=host['host_id'],
                               cpu=host['cpu'],
                               ram=host['ram'],
                               cluster=host['cluster_id']
                               )

        host_record.save()

    for vm_id, vm in data["vms"].items():
        try:
            vm_record = VM.objects.get(vm_id=vm['vm_id'])
            vm_record.cpu = vm["cpu"]
            vm_record.ram = vm["ram"]
            vm_record.host = Host.objects.get(host_id=vm['host_id'])
        except VM.DoesNotExist:
            vm_record = VM(vm_id=vm['vm_id'],
                           cpu=vm['cpu'],
                           ram=vm['ram'],
                           host=Host.objects.get(host_id=vm['host_id'])
                           )
        vm_record.save()

    return data

@login_required
def load_cloud_conf(request):
    if request.method == 'POST':
        if not request.POST.get('is_new_config', None):
            load_new_cloud_conf()

            messages.success(request, "Cloud configuration was successfully loaded!")
            return HttpResponseRedirect("/")
        else:
            if request.POST.get('data_changes'):
                update_cloud_conf(request.POST.get('data_changes'))
                messages.success(request, "Configuration was updated successfully!")
            else:
                messages.error(request, "Unable to change configuration!")

            return HttpResponseRedirect("/")
    else:
        if (Cluster.objects.count() == 0) and (Host.objects.count() == 0) and (VM.objects.count() == 0):
            if HostGroup.objects.count() == 0:
                return TemplateResponse(request, "load_cloud_conf.html", {"is_empty_conf": True, "is_host_group_empty": True})
            else:
                return TemplateResponse(request, "load_cloud_conf.html", {"is_empty_conf": True, "is_host_group_empty": False})
        else:
            return TemplateResponse(request, "load_cloud_conf.html", {"is_empty_conf": False, "changes": get_cloud_conf_changes()})

@login_required
def drop_cloud_conf(request):
    if request.POST.get('post'):
        Cluster.objects.all().delete()
        HostGroup.objects.all().delete()
        Host.objects.all().delete()
        VM.objects.all().delete()

        messages.success(request, "Cloud configuration was successfully dropped!")
        return HttpResponseRedirect("/")
    else:
        return TemplateResponse(request, "delete_cloud_config_confirmation.html")

@login_required
def get_host_info(request):
    if request.method == 'POST' and request.is_ajax():
        host_id = request.POST.get('host_id', None)

        if host_id:
            host_id = int(host_id)
            cloud = common.get_cloud_handler()
            host = cloud.get_host_repr(host_id)

            response = {'id': host['id'], 'cpu': host['usage_cpu']['max'], 'ram': host['usage_mem']['max'], 'cluster_id': host['cluster_id']}

            messages.success(request, "Host information was synchronized successfully!")
            return response_with_messages(messages, response, request)
        else:
            return HttpResponse("host_id is empty")
    else:
        return HttpResponse("Wrong request")

@login_required
def get_cluster_info(request):
    if request.method == 'POST' and request.is_ajax():
        cluster_id = request.POST.get('cluster_id', None)

        if cluster_id:
            cluster_id = int(cluster_id)
            cloud = common.get_cloud_handler()
            cluster = cloud.get_cluster_repr(cluster_id)

            response = {'id': cluster['id'], 'name': cluster['name']}

            messages.success(request, "Cluster information was synchronized successfully!")

            return response_with_messages(messages, response, request)
        else:
            return HttpResponse("cluster_id is empty")
    else:
        return HttpResponse("Wrong request")

@login_required
def get_vm_info(request):
    if request.method == 'POST' and request.is_ajax():
        vm_id = request.POST.get('vm_id', None)

        if vm_id:
            vm_id = int(vm_id)
            cloud = common.get_cloud_handler()
            vm = cloud.get_vm_repr(vm_id)

            response = {'id': vm['id'], 'cpu': vm['cpu_req'], 'ram': vm['mem_req'], 'host': vm['hid']}

            messages.success(request, "VM information was synchronized successfully!")
            return response_with_messages(messages, response, request)
        else:
            return HttpResponse("vm_id is empty")
    else:
        return HttpResponse("Wrong request")

@login_required
def get_host_metrics(request):
    if request.method == 'POST' and request.is_ajax():
        host_id = request.POST.get('host_id', None)

        if host_id:
            grafana_endpoint = settings.GRAFANA_ENDPOINT
            host_id = int(host_id)
            cloud = common.get_cloud_handler()
            host = cloud.get_host_repr(host_id)
            host_name = host['name']
            date_to = int(round(time.time() * 1000))
            date_from = date_to - 86400000

            date_to = str(date_to)
            date_from = str(date_from)

            content = render_to_string('metrics_host.html', {'grafana_endpoint': grafana_endpoint, 'date_from': date_from, 'date_to':date_to, 'host_name': host_name});
            response = {'html': content, 'date_from': date_from, 'date_to':date_to}

            return response_with_messages(messages, response, request)
        else:
            return HttpResponse("host_id is empty")
    else:
        return HttpResponse("Wrong request")

@login_required
def get_vm_metrics(request):
    if request.method == 'POST' and request.is_ajax():
        vm_id = request.POST.get('vm_id', None)

        if vm_id:
            grafana_endpoint = settings.GRAFANA_ENDPOINT

            date_to = int(round(time.time() * 1000))
            date_from = date_to - 86400000
            date_to = str(date_to)
            date_from = str(date_from)

            content = """
                <div class="row"">
                    <div class="col-sm-8">
                        <iframe src=" """ + grafana_endpoint + """/dashboard-solo/db/vm-cpu-mem-load?refresh=15s&orgId=1&panelId=1&from=""" + date_from + """&to=""" + date_to +"""&var-vm=""" + vm_id + """&theme=light" width="450" height="200" frameborder="0"></iframe><br>
                        <iframe src=" """ + grafana_endpoint + """/dashboard-solo/db/vm-cpu-mem-load?refresh=15s&orgId=1&panelId=2&from=""" + date_from + """&to=""" + date_to +"""&var-vm=""" + vm_id + """&theme=light" width="450" height="200" frameborder="0"></iframe><br>
                    </div>
                </div>
                """
            content = render_to_string('metrics_vm.html', {'grafana_endpoint': grafana_endpoint, 'date_from': date_from, 'date_to':date_to, 'vm_id': vm_id});
            response = {'html': content, 'date_from': date_from, 'date_to':date_to}

            return response_with_messages(messages, response, request)
        else:
            return HttpResponse("vm_id is empty")
    else:
        return HttpResponse("Wrong request")
