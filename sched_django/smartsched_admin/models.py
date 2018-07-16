from django.db import models
from django.utils.translation import ugettext as _

class Cluster(models.Model):
    cluster_id = models.IntegerField(default=0, unique=True)
    cluster_name = models.CharField(max_length=200)

    def admin_sync_cluster(self):
        return '<div class="btn btn-primary btn-sm" id="id_admin_sync_cluster" role="group" aria-label="..."><i class="fa fa-refresh" id="sync_cluster_spinner" aria-hidden="True"></i> ' + _('Sync cluster info') + '</div>'

    admin_sync_cluster.allow_tags = True
    admin_sync_cluster.short_description = _("Sync cluster info")

    def __str__(self):
        return str(self.cluster_id)

class HostGroup(models.Model):
    host_group_name = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.host_group_name

class Host(models.Model):
    cluster = models.IntegerField(default=None)
    host_group = models.ForeignKey(HostGroup, blank=True, null=True, default=None)
    host_id = models.IntegerField(default=0, unique=True)
    cpu = models.IntegerField(default=0)
    ram = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def admin_sync_host(self):
        return '<div class="btn btn-primary btn-sm" id="id_admin_sync_host" role="group" aria-label="..."><i class="fa fa-refresh" id="sync_host_spinner" aria-hidden="True"></i> ' + _('Sync host info') + '</div>'
    def performance_metrics(self):
        return """
              <div class="panel panel-default" id="performance_metrics">
                <div class="panel-heading">
                  <h4 class="panel-title">
                    <a data-toggle="collapse" href="#host_performance_metrics">Show performance metrics</a>
                  </h4>
                </div>
                <div id="host_performance_metrics" class="panel-collapse collapse">
                  <div id= "host_perf_body" class="panel-body" style="text-align:center;"></div>
                </div>
              </div>
        """

    performance_metrics.allow_tags = True
    performance_metrics.short_description = _("Show performance metrics")

    admin_sync_host.allow_tags = True
    admin_sync_host.short_description = _("Sync host info")

    def __str__(self):
        return str(self.host_id)

class StrategySetting(models.Model):
    strategy_name = models.CharField(max_length=200)
    setting_name = models.CharField(max_length=200)
    setting_value = models.CharField(max_length=200)

    def __str__(self):
        return '%s: %s = %s' % (self.strategy_name, self.setting_name, self.setting_value)

class VM(models.Model):
    vm_id = models.IntegerField(default=0, unique=True)
    host = models.ForeignKey(Host)
    cpu = models.FloatField(default=0)
    ram = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def admin_sync_vm(self):
        return '<div class="btn btn-primary btn-sm" id="id_admin_sync_vm" role="group" aria-label="..."><i class="fa fa-refresh" id="sync_vm_spinner" aria-hidden="True"></i> ' + _('Sync VM info') + '</div>'

    def performance_metrics(self):
        return """
              <div class="panel panel-default" id="performance_metrics">
                <div class="panel-heading">
                  <h4 class="panel-title">
                    <a data-toggle="collapse" href="#vm_performance_metrics">Show performance metrics</a>
                  </h4>
                </div>
                <div id="vm_performance_metrics" class="panel-collapse collapse">
                  <div id= "vm_perf_body" class="panel-body" style="text-align:center;"></div>
                </div>
              </div>
        """

    performance_metrics.allow_tags = True
    performance_metrics.short_description = _("Show performance metrics")
    admin_sync_vm.allow_tags = True
    admin_sync_vm.short_description = _("Sync VM info")

    def __str__(self):
        return str(self.vm_id)
