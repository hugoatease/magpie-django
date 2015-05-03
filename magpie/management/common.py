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

import ippool
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string

from magpie.management.models import UserConfig, UserSettings, BandwidthAct, ConnectionLog
from magpie.servers.models import Subnet, Address, Server

def access_get(user, id=None, server=None, token=None):
    if id is not None:
        return UserConfig.objects.get(user=user, id=id)
    
    if server is not None and token is not None:
        return UserConfig.objects.get(user=user, server=server, token=token)
    
    return UserConfig.objects.filter(user=user)
    
def access_create(user, server):
    if server.type == 'TUN':
        pool = ippool.Pool()
    else:
        pool = ippool.Pool(False)

    for subnet in server.subnets.all():
        pool.addSubnet(subnet.address, subnet.cidr)
        
        for address in subnet.addresses.all():
            pool.exclude(address.address)
    
    address = pool.available()
    subnet = Subnet.objects.get(address=address['subnet'], cidr=address['cidr'])
    
    address = Address(subnet=subnet, address=address['address'])
    address.save()
    
    token = get_random_string(length=20)
    
    uconf = UserConfig(server=server, address=address, user=user, token=token)
    uconf.save()
    
    return True

def access_delete(user, id):
    uconf = UserConfig.objects.get(id=id, user=user)
    uconf.address.delete()
    uconf.delete()

def bandwidth_reports(user):
    return BandwidthAct.objects.filter(user=user)

def bandwidth_used(user):
    traffic = 0
    for server in Server.objects.all():
        try:
            serverbw = BandwidthAct.objects.get(user=user, server=server, end__gt=datetime.now())
            
            traffic += serverbw.bytes_received + serverbw.bytes_sent
        except (BandwidthAct.DoesNotExist, BandwidthAct.MultipleObjectsReturned):
            pass
    
    return traffic

def log_create(user, server, origin):
    log = ConnectionLog(user=user, server=server, origin=origin)
    log.save()

def log_optout(user, choice=None):
    settings = UserSettings.objects.get(user=user)
    
    if choice not in [True, False]:
        return settings.log_optout
    else:
        settings.log_optout = choice
        settings.save()

def log_list(user):
    return ConnectionLog.objects.filter(user=user)

def log_clear(user):
    logs = log_list(user)
    for log in logs:
        log.delete()

def access_set_state(userconfig, connected, origin=None):
    if connected and not log_optout(userconfig.user) and not userconfig.connected:
        userconfig.current_origin = origin
        userconfig.current_date = datetime.now()
    
    userconfig.connected = connected
    userconfig.save()

def bandwidth_add(user, server, received, sent):
    try:
        act = BandwidthAct.objects.get(user=user, server=server, end__gt=datetime.now())
    except BandwidthAct.DoesNotExist:
        begin = datetime.now()
        
        try:
            end = BandwidthAct.objects.filter(user=user, end__gt=datetime.now())[0].end
        except:
            end = begin + timedelta(days=31)
        
        act = BandwidthAct(user=user, server=server, begin=begin, end=end, bytes_received=0, bytes_sent=0)

    act.bytes_received += int(received)
    act.bytes_sent += int(sent)
    
    act.save()
