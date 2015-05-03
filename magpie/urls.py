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

from django.conf.urls import patterns, include, url
from django.contrib import admin
from oauth2_provider.views import TokenView, AuthorizationView
from magpie.api.routers import router
admin.autodiscover()

handler500 = 'magpie.views.handler500'

urlpatterns = patterns('',
    url(r'^$', 'magpie.views.index', name='index'),
    url(r'^servers/', include('magpie.servers.urls')),
    url(r'^account/', include('magpie.account.urls')),
    url(r'^vpn/', include('magpie.management.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^oauth/authorize/$', AuthorizationView.as_view(), name="authorize"),
    url(r'^oauth/token/$', TokenView.as_view(), name="token"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)