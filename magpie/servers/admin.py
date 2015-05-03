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

from django.contrib import admin
from models import Server, Subnet, Address

class SubnetsInline(admin.StackedInline):
    model = Subnet
    extra = 1

class ServerAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'address', 'port', 'protocol')
    inlines = [SubnetsInline]

class SubnetAdmin(admin.ModelAdmin):
    list_display = ('server', 'address', 'cidr')

admin.site.register(Server, ServerAdmin)
admin.site.register(Subnet, SubnetAdmin)
admin.site.register(Address)