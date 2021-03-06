# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsched_admin', '0004_remove_cluster_host_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='cluster_id',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='cluster',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='host',
            name='host_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='smartsched_admin.HostGroup'),
        ),
        migrations.AlterField(
            model_name='host',
            name='host_id',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='host_id',
            field=models.IntegerField(blank=True, default=0, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='vm',
            name='cpu',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vm',
            name='vm_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
