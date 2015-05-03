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

from oauth2_provider.oauth2_validators import OAuth2Validator
from django.conf import settings


class ApiOAuth2Validator(OAuth2Validator):
    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return 'read write'

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        if 'service' in scopes:
            if client.service:
                return True
            else:
                return False

        return set(scopes).issubset(set(settings.OAUTH2_PROVIDER['SCOPES']))