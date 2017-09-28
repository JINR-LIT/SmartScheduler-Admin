from django.contrib import admin
from django.utils.html import format_html

from .models import *
from django.conf import settings

# Register your models here.

class ClusterAdmin(admin.ModelAdmin):
    list_display = ('cluster_id', 'cluster_name')

    readonly_fields = ('admin_sync_cluster', )

    class Media:
        js = ('js/cloud_api.js',)

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('host_group_name',)

class HostAdmin(admin.ModelAdmin):
    list_display = ('host_id', 'cluster', 'host_group', 'cpu', 'ram', 'rank',)
    list_editable = ('rank', "host_group", )
    readonly_fields = ('admin_sync_host',)

    if hasattr(settings, "GRAFANA_ENDPOINT"):
        list_display += ('metrics',)
        readonly_fields += ('performance_metrics',)

    def metrics(self, obj):
        return format_html(
            '<a class="button host_metrics" id="'+ str(obj.host_id) +'" data-toggle="modal" data-target="#host_metrics_'+str(obj.host_id)+'"><i class="fa fa-tachometer" aria-hidden="true"></i></a>' + """
                <div id='host_metrics_""" +str(obj.host_id)+"""' class="modal fade" role="dialog">
                  <div class="modal-dialog modal-lg" id="performance_metrics">

                    <!-- Modal content-->
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <h4 class="modal-title">Host <div id='modal_host_id' style='display: inline;'> """ + str(obj.host_id) + """ </div>metrics</h4>
                      </div>
                      <div class="modal-body">
                        <div id= "host_perf_body" class="panel-body" style="text-align:center;"></div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      </div>
                    </div>

                  </div>
                </div>
            """
        )

    class Media:
        js = ('js/cloud_api.js',)

class VMAdmin(admin.ModelAdmin):
    list_display = ('vm_id', 'host', 'cpu', 'ram', 'rank')
    list_editable = ('rank',)
    readonly_fields = ('admin_sync_vm', )

    if hasattr(settings, "GRAFANA_ENDPOINT"):
        list_display += ('metrics',)
        readonly_fields += ('performance_metrics',)

    def metrics(self, obj):
        return format_html(
            '<a class="button vm_metrics" id="'+ str(obj.vm_id) +'" data-toggle="modal" data-target="#vm_metrics_'+str(obj.vm_id)+'"><i class="fa fa-tachometer" aria-hidden="true"></i></a>' + """
                <div id='vm_metrics_""" +str(obj.vm_id)+"""' class="modal fade" role="dialog">
                  <div class="modal-dialog modal-lg">

                    <!-- Modal content-->
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <h4 class="modal-title">VM <div id='modal_vm_id' style='display: inline;'> """ + str(obj.vm_id) + """ </div>metrics</h4>
                      </div>
                      <div class="modal-body">
                        <div id= "vm_perf_body" class="panel-body" style="text-align:center;"></div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      </div>
                    </div>

                  </div>
                </div>
            """
        )

    class Media:
        js = ('js/cloud_api.js',)

admin.site.register(Cluster, ClusterAdmin)
admin.site.register(HostGroup, HostGroupAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(VM, VMAdmin)
