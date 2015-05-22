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

from magpie.management.models import UserConfig
import serializers
from django.contrib.auth.models import User
import magpie.management.common as management
from magpie.api.permissions import IsAdminOrAuthenticatedRead
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasScope
from models import Server, Subnet, Address


class ServerViewSetPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if TokenHasScope().has_permission(request, view) and request.method in permissions.SAFE_METHODS:
            return True
        else:
            return IsAdminOrAuthenticatedRead().has_permission(request, view)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    lookup_field = 'name'
    serializer_class = serializers.ServerSerializer
    permission_classes = [ServerViewSetPermissions]
    required_scopes = ['service']

    @detail_route(methods=['post'], permission_classes=[TokenHasScope])
    def connect(self, request, *args, **kwargs):
        server = self.get_object()
        req = serializers.ConnectRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)

        try:
            user = User.objects.get(username=req.validated_data['username'])
        except:
            raise exceptions.ValidationError(detail="User matching username not found")

        try:
            uconf = management.access_get(user, server=server, token=req.validated_data['token'])
        except:
            raise exceptions.PermissionDenied(detail="Invalid configuration token")

        if not management.log_optout(user) and not uconf.connected:
            management.log_create(user, server, req.validated_data['origin'])

        management.access_set_state(uconf, True, req.validated_data['origin'])
        mask = uconf.address.subnet.get_netmask()

        return Response(data={'address': uconf.address.address, 'type': server.type, 'mask': mask})

    @detail_route(methods=['post'], permission_classes=[TokenHasScope])
    def disconnect(self, request, *args, **kwargs):
        server = self.get_object()
        req = serializers.DisconnectRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)

        try:
            user = User.objects.get(username=req.validated_data['username'])
        except:
            raise exceptions.ValidationError("User matching username not found")

        management.bandwidth_add(user, server, req.validated_data['received'], req.validated_data['sent'])

        address = Address.objects.get(subnet__server=server, address=request.POST['address'])
        uconf = UserConfig.objects.get(server=server, user=user, address=address)
        management.access_set_state(uconf, False)

        return Response(status=status.HTTP_202_ACCEPTED)


class SubnetViewSet(viewsets.ModelViewSet):
    queryset = Subnet.objects.all()
    serializer_class = serializers.SubnetSerializer
    permission_classes = [IsAdminOrAuthenticatedRead]