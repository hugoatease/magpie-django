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

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from models import UserSettings
from magpie.servers.models import Server
from common import access_create

@receiver(user_logged_in)
def create_UserSettings(sender, **kwargs):
    user = kwargs['user']

    if UserSettings.objects.filter(user=user).count() > 0:
        return
    
    settings = UserSettings(user=user)
    settings.save()
    
    if Server.objects.count() > 0:
        server = Server.objects.all()[0]
        access_create(user, server)