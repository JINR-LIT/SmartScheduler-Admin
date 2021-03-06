# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_name', models.CharField(max_length=200)),
                ('host_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.IntegerField(default=0)),
                ('ram', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('cluster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smartsched_admin.Cluster')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.IntegerField(default=0)),
                ('ram', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartsched_admin.Host')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='host_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smartsched_admin.HostGroup'),
        ),
    ]
