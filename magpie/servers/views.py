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

from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from models import Server
from ipaddr import IPNetwork
from django.conf import settings
from django.shortcuts import get_object_or_404

@login_required
def servers(request, name=None):
    servers = Server.objects.all()
    server = servers[0]
    networks = list()
    
    if name is not None:
        server = get_object_or_404(Server, name=name)
        
    for subnet in server.subnets.all():
        net = {'subnet' : subnet.address + u'/' + unicode(subnet.cidr)}
        net['available'] = (IPNetwork(net['subnet']).numhosts / 4) - len(subnet.addresses.all())
        networks.append(net)

    return render(request, "servers/server.html", {'servers' : servers, 'server' : server, 'networks' : networks})

@login_required
def config(request, name):
    server = get_object_or_404(Server, name=name)
    response = render_to_response("servers/config.ovpn", {'server' : server})
    
    response['Content-Type'] = "text/plain" + '; charset=' + settings.DEFAULT_CHARSET
    response['Content-disposition'] = 'attachment' 
    return response

@login_required
def authority(request, name):
    server = get_object_or_404(Server, name=name)
    response = render_to_response("servers/ca.pem", {'server' : server})
    
    response['Content-Type'] = "text/plain" + '; charset=' + settings.DEFAULT_CHARSET
    response['Content-disposition'] = 'attachment' 
    return response