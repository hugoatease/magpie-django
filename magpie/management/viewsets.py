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

import common
import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.decorators import list_route


class UserConfigViewSet(viewsets.ReadOnlyModelViewSet,
                        mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.UserConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return common.access_get(self.request.user)

    def perform_create(self, serializer):
        common.access_create(self.request.user, serializer.validated_data['server'])

    def perform_destroy(self, instance):
        common.access_delete(self.request.user, instance.id)


class BandwidthActViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BandwidthActSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return common.bandwidth_reports(self.request.user)

    @list_route(methods=['get'])
    def used(self, request):
        return Response({'used': common.bandwidth_used(request.user)})


class ConnectionLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ConnectionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return common.log_list(self.request.user)

    @list_route(methods=['post'])
    def clear(self, request):
        common.log_clear(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)