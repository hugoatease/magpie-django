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

urlpatterns = patterns('magpie.account.views',
    url(r'^$', 'account', name='account_account'),
    url(r'^signup/$', 'signup_begin', name='account_signup_begin'),
    url(r'^signup/(?P<token>\w{1,})/$', 'signup', name='account_signup'),
    url(r'^invite/$', 'invite', name='account_invite'),
    url(r'^mail/(?P<token>\w{1,})/$', 'mailvalidation', name='account_mailvalidation'),
    url(r'^recover/$', 'password_recovery_begin', name='account_password_recovery_begin'),
    url(r'^recover/(?P<token>\w{1,})/$', 'password_recovery', name='account_password_recovery'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='account_login'),
    url(r'^logout/$', 'logout', {'next_page' : '/'}, name='account_logout'),
)
