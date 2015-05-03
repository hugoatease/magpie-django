# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.IPAddressField()),
            ],
            options={
                'verbose_name': 'Adresse IP',
                'verbose_name_plural': 'Addresses IP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('display_name', models.CharField(max_length=64)),
                ('address', models.IPAddressField()),
                ('port', models.IntegerField()),
                ('protocol', models.CharField(max_length=64, choices=[(b'TCP', b'TCP'), (b'UDP', b'UDP')])),
                ('type', models.CharField(max_length=64, choices=[(b'TUN', b'TUN'), (b'TAP', b'TAP')])),
                ('cipher', models.CharField(max_length=64)),
                ('authority', models.TextField()),
                ('directives', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['display_name'],
                'verbose_name': 'Serveur',
                'verbose_name_plural': 'Serveurs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.IPAddressField()),
                ('cidr', models.IntegerField()),
                ('server', models.ForeignKey(related_name='subnets', to='servers.Server')),
            ],
            options={
                'verbose_name': 'Sous-r\xe9seau',
                'verbose_name_plural': 'Sous-r\xe9seaux',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='subnet',
            field=models.ForeignKey(related_name='addresses', to='servers.Subnet'),
            preserve_default=True,
        ),
    ]
