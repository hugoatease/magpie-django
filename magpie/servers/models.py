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
from ipaddr import IPNetwork

charlength = 64

class Server(models.Model):
    class Meta:
        verbose_name = "Serveur"
        verbose_name_plural = "Serveurs"
        ordering = ['display_name']
        
    name = models.CharField(max_length=charlength, unique=True)
    display_name = models.CharField(max_length=charlength)
    address = models.GenericIPAddressField(protocol='IPv4')
    port = models.IntegerField()
    protocol = models.CharField(max_length=charlength, choices=(("TCP", "TCP"), ("UDP", "UDP")))
    type = models.CharField(max_length=charlength, choices=(('TUN', 'TUN'), ('TAP', 'TAP')))
    cipher = models.CharField(max_length=charlength)
    authority = models.TextField()
    directives = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.display_name

class Subnet(models.Model):
    class Meta:
        verbose_name = "Sous-réseau"
        verbose_name_plural = "Sous-réseaux"
        
    server = models.ForeignKey(Server, related_name="subnets")
    
    address = models.GenericIPAddressField(protocol='IPv4')
    cidr = models.IntegerField()
    
    def get_netmask(self):
        net = self.address + u"/" + unicode(self.cidr)
        net = IPNetwork(net)
        return unicode(net.netmask)
        

class Address(models.Model):
    class Meta:
        verbose_name = "Adresse IP"
        verbose_name_plural = "Addresses IP"
        
    subnet = models.ForeignKey(Subnet, related_name="addresses")
    address = models.GenericIPAddressField(protocol='IPv4')
    
    def __unicode__(self):
        return self.address
