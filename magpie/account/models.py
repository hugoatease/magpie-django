# -*- coding: utf-8 -*-
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

from django.db import models
from django.contrib.auth.models import User

charlength = 64

class Invite(models.Model):
    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        ordering = ['-date']

    date = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    token = models.CharField(max_length=charlength)

class MailValidation(models.Model):
    class Meta:
        verbose_name = "Validation d'addresse e-mail"
        verbose_name_plural = "Validations d'addresse e-mail"
    
    user = models.ForeignKey(User, related_name="mailvalidations")
    date = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    token = models.CharField(max_length=charlength)

class PasswordRecovery(models.Model):
    user = models.ForeignKey(User, related_name="passwordrecoveries")
    date = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    token = models.CharField(max_length=charlength)