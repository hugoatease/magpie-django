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

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

def unique_email(email):
    unique = True
    
    user = User.objects.filter(email=email)
    if user.count() != 0:
        unique = False
    
    return unique

class VPNProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

class VPNEmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        
    email = forms.EmailField(label=_("Email address"))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        if not unique_email(data):
            raise forms.ValidationError(_("Provided email address is already matching an user"))
        
        return data

class VPNBeginSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
    
    email = forms.EmailField(label=_("Email address"))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        if not unique_email(data):
            raise forms.ValidationError(_("Provided email address is already matching an user"))
        
        return data

class VPNSignupForm(UserCreationForm):        
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')
    
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

class PasswordRecoveryForm(forms.ModelForm):
    error_messages = {
        'unknown_user': _("Provided email address doesn't match any user")
    }
    
    class Meta:
        model = User
        fields = ['email']
        
    email = forms.EmailField(label=_("Email address"))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        try:
            self.user = User.objects.get(email=self.cleaned_data['email'])
        except:
            self.user = None
            raise forms.ValidationError(self.error_messages['unknown_user'])
        
        return data

class VPNInviteForm(forms.Form):
    email = forms.EmailField(label=_("Email address"))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        if not unique_email(data):
            raise forms.ValidationError(_("Provided email address is already matching an user"))
        
        return data