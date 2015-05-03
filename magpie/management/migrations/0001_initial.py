# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BandwidthAct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('begin', models.DateField()),
                ('end', models.DateField()),
                ('bytes_sent', models.BigIntegerField()),
                ('bytes_received', models.BigIntegerField()),
                ('server', models.ForeignKey(related_name='bandwithacts', to='servers.Server')),
                ('user', models.ForeignKey(related_name='bandwithacts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user', '-begin'],
                'verbose_name': 'Consommation de BP',
                'verbose_name_plural': 'Consommation de BP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConnectionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('origin', models.IPAddressField()),
                ('server', models.ForeignKey(related_name='connectionlogs', to='servers.Server')),
                ('user', models.ForeignKey(related_name='connectionlogs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Historique de connexion',
                'verbose_name_plural': 'Historique de connexions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('connected', models.BooleanField(default=False)),
                ('current_origin', models.IPAddressField(null=True, blank=True)),
                ('current_date', models.DateTimeField(null=True, blank=True)),
                ('address', models.ForeignKey(related_name='userconfigs', to='servers.Address')),
                ('server', models.ForeignKey(related_name='userconfigs', to='servers.Server')),
                ('user', models.ForeignKey(related_name='userconfigs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': "Configuration d'acc\xe8s",
                'verbose_name_plural': "Configurations d'acc\xe8s",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_optout', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='usersettings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': 'Configuration utilisateur',
                'verbose_name_plural': 'Configurations utilisateur',
            },
            bases=(models.Model,),
        ),
    ]
