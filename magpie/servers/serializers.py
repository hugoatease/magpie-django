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
from models import Server, Subnet, Address

class SubnetSerializer(serializers.ModelSerializer):
    server = serializers.SlugRelatedField(slug_field='name', queryset=Server.objects.all())

    class Meta:
        model = Subnet
        fields = ('id', 'server', 'address', 'cidr')

class AddressSerializer(serializers.ModelSerializer):
    subnet = SubnetSerializer()
    class Meta:
        model = Address
        fields = ('id', 'address', 'subnet')

class ServerSerializer(serializers.ModelSerializer):
    subnets = SubnetSerializer(many=True)
    class Meta:
        model = Server
        fields = ('name', 'display_name', 'address', 'port', 'protocol',
            'type', 'cipher', 'subnets')

class ConnectRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    token = serializers.CharField()
    origin = serializers.CharField()


class DisconnectRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    address = serializers.CharField()
    received = serializers.IntegerField()
    sent = serializers.IntegerField()