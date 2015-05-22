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

from rest_framework import serializers
from models import UserConfig, BandwidthAct, ConnectionLog, UserSettings
from magpie.servers.models import Server
from magpie.servers.serializers import AddressSerializer


class UserConfigSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    server = serializers.SlugRelatedField(slug_field='name', queryset=Server.objects.all())

    class Meta:
        model = UserConfig
        fields = ('id', 'server', 'address', 'token')
        read_only_fields = ('address', 'token')


class BandwidthActSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandwidthAct
        fields = ('begin', 'end', 'bytes_sent', 'bytes_received')


class ConnectionLogSerializer(serializers.ModelSerializer):
    server = serializers.SlugRelatedField(slug_field='name', queryset=Server.objects.all())

    class Meta:
        model = ConnectionLog
        fields = ('server', 'date', 'origin')

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ('accesses', 'log_optout')