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

from django.conf.urls import patterns, url

urlpatterns = patterns('magpie.management.views',
    url(r'^$', 'access', name='management_access'),
    url(r'^bandwidth/$', 'bandwidth', name='management_bandwidth'),
    url(r'^logs/$', 'logs', name='management_logs'),
    url(r'^config/(?P<name>\D{1,}).zip$', 'getconfig', name='management_getconfig'),
)
