# -*- coding: utf-8 -*-
# Copyright 2013-2015 Hugo Caille
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.contrib.auth.models import User

charlength = 64

class UserConfig(models.Model):
    class Meta:
        app_label = 'management'
        verbose_name = "Configuration d'accès"
        verbose_name_plural = "Configurations d'accès"
        ordering = ['user']

    server = models.ForeignKey('servers.Server', related_name="userconfigs")
    address = models.ForeignKey('servers.Address', related_name="userconfigs")
    user = models.ForeignKey(User, related_name="userconfigs")
    
    token = models.CharField(max_length=charlength)
    
    connected = models.BooleanField(default=False)
    current_origin = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    current_date = models.DateTimeField(null=True, blank=True)

class BandwidthAct(models.Model):
    class Meta:
        app_label = 'management'
        verbose_name = "Consommation de BP"
        verbose_name_plural = "Consommation de BP"
        ordering = ['user', '-begin']
    
    user = models.ForeignKey(User, related_name="bandwithacts")
    server = models.ForeignKey('servers.Server', related_name="bandwithacts")
    
    begin = models.DateField()
    end = models.DateField()
    
    bytes_sent = models.BigIntegerField()
    bytes_received = models.BigIntegerField()

class ConnectionLog(models.Model):
    class Meta:
        app_label = 'management'
        verbose_name = "Historique de connexion"
        verbose_name_plural = "Historique de connexions"
        ordering = ['-date']

    user = models.ForeignKey(User, related_name="connectionlogs")
    server = models.ForeignKey('servers.Server', related_name="connectionlogs")
    date = models.DateTimeField(auto_now=True)
    origin = models.GenericIPAddressField(protocol='IPv4')

class UserSettings(models.Model):
    class Meta:
        app_label = 'management'
        verbose_name = "Configuration utilisateur"
        verbose_name_plural = "Configurations utilisateur"
        ordering = ['user']

    user = models.ForeignKey(User, related_name="usersettings")
    log_optout = models.BooleanField(default=False)