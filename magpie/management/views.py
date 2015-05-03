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

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from models import UserConfig
from magpie.servers.models import Server

import common

from zipfile import ZipFile
from StringIO import StringIO

class AccessForm(ModelForm):
    class Meta:
        model = UserConfig
        fields = ('server',)

@login_required
def access(request):
    userconfigs = common.access_get(request.user)
    
    form = AccessForm()
        
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            common.access_create(request.user, form.cleaned_data['server'])
        if request.POST.has_key('id'):
            common.access_delete(request.user, request.POST['id'])
            form = AccessForm()

    return render(request, "management/access.html", {'form' : form, 'userconfigs' : userconfigs})

@login_required
def bandwidth(request):
    bwacts = common.bandwidth_reports(request.user)
    
    traffic = common.bandwidth_used(request.user)
    
    return render(request, "management/bandwidth.html", {'bwacts' : bwacts, 'traffic' : traffic})

@login_required
def logs(request):
    if request.method == 'POST' and request.POST.has_key("optout"):
        common.log_optout(request.user, not common.log_optout(request.user))
    
    if request.method == 'POST' and request.POST.has_key("clear_history"):
        common.log_clear(request.user)
    
    logs = common.log_list(request.user)
    
    optout = common.log_optout(request.user)
    return render(request, "management/logs.html", {'logs' : logs, 'optout' : optout})

@login_required
def getconfig(request, name):
    server = get_object_or_404(Server, name=name)
    uconf = common.access_get(request.user, id=request.POST['id'])
    
    username = uconf.user.username
    token = uconf.token
    
    f = StringIO()
    zip = ZipFile(f, "w")
    
    zip.writestr(server.name + ".ovpn", str(render_to_string("servers/config.ovpn", {'server' : server, 'bundled_credentials' : True})))
    zip.writestr(server.name + ".pem", str(render_to_string("servers/ca.pem", {'server' : server})))
    zip.writestr(server.name + ".txt", str(render_to_string("management/access.txt", {'username' : username, 'token' : token})))
    
    zip.writestr(server.name + ".tblk/Contents/Resources/config.ovpn", str(render_to_string("servers/config.ovpn", {'server' : server, 'bundled_credentials' : False})))
    zip.writestr(server.name + ".tblk/Contents/Resources/" + server.name + ".pem", str(render_to_string("servers/ca.pem", {'server' : server})))
    
    zip.close()
    
    response = HttpResponse(f.getvalue())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment"
    return response
