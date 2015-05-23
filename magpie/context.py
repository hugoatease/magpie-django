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

from django.conf import settings
from management.models import UserConfig

def siteconf(request):
    return {
        'BRAND_NAME': getattr(settings, 'BRAND_NAME', 'Magpie'),
        'SELF_REGISTER': getattr(settings, 'SELF_REGISTER', False)
    }

def is_on_vpn(request):
    if request.user.is_authenticated():
        active = UserConfig.objects.filter(user=request.user, connected=True)
        count = active.count()
        return {'VPN_CONNECTED': count, 'VPN_ACTIVE': active}
    
    return {'VPN_CONNECTED': False}