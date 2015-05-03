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

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from models import Invite, MailValidation, PasswordRecovery

from forms import *
from signals import user_created

from django.template.context import RequestContext

def mailsubject(subject, context):
    return context['BRAND_NAME'] + " - " + subject

def send_branded_email(subject, message, receipent, context):
    subject = mailsubject(subject, context)
    sender = getattr(settings, 'SERVER_EMAIL', 'magpie@example.com')
    send_mail(subject, message, sender, [receipent])
    

@login_required
def account(request):
    context = RequestContext(request)
    
    passwordform = PasswordChangeForm(request.user)
    profileform = VPNProfileForm(instance=request.user)
    emailform = VPNEmailChangeForm(instance=request.user)
    inviteform = VPNInviteForm()
    
    success = False
    success_message = None
    
    if request.method == 'POST' and request.POST.has_key("password"):
        passwordform = PasswordChangeForm(request.user, request.POST)
        
        if passwordform.is_valid():
            request.user.set_password(passwordform.cleaned_data['new_password1'])
            request.user.save()
            success = True
    
    if request.method == 'POST' and request.POST.has_key("profile"):    
        profileform = VPNProfileForm(request.POST, instance=request.user)
        
        if profileform.is_valid():
            profileform.save()
            success = True
    
    if request.method == 'POST' and request.POST.has_key("emailchange"):
        emailform = VPNEmailChangeForm(request.POST, instance=request.user)
        
        if emailform.is_valid():
            token = get_random_string(length=50)
            validation = MailValidation(user=request.user, token=token, email=emailform.cleaned_data['email'])
            validation.save()
            
            url = request.build_absolute_uri(reverse('account_mailvalidation', args=[token]))
            message = render_to_string("account/mailvalidation.txt", {'url' : url}, context_instance=context)
            send_branded_email("Validation d'adresse e-mail", message, emailform.cleaned_data['email'], context)
            
            success = True
            success_message = "Un email vous a été envoyé contenant un lien permettant de valider votre nouvelle adresse."

    if request.method == 'POST' and request.POST.has_key('invitechange'):
        inviteform = VPNInviteForm(request.POST)
        if inviteform.is_valid():
            token = get_random_string(length=50)

            invite = Invite(token=token, email=inviteform.cleaned_data['email'])
            invite.save()

            url = request.build_absolute_uri(reverse('account_signup', args=[token]))

            message = render_to_string("account/invitemsg.txt", {'url' : url}, context_instance=context)

            send_branded_email("Invitation", message, inviteform.cleaned_data['email'], context)

            success = True
            success_message = "L'invitation a bien été envoyée."

    return render(request, "account/account.html",
                  {'passwordform' : passwordform, 
                   'profileform' : profileform,
                   'emailform' : emailform,
                   'invite_form': inviteform,
                   'success' : success,
                   'success_message' : success_message})

def signup(request, token):
    try:
        invite = Invite.objects.get(token=token)
    except Invite.DoesNotExist:
        return redirect('django.contrib.auth.views.login')
    
    if invite.used:
        return redirect('django.contrib.auth.views.login')
    
    if request.method == 'GET':
        form = VPNSignupForm()
        
    elif request.method == 'POST':
        form = VPNSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], invite.email, data['password2'], first_name=data['first_name'], last_name=data['last_name'])
            
            user_created.send(signup, user=user)

            invite.delete()
            
            # Automatic login of created user.
            user = authenticate(username=data['username'], password=data['password2'])
            login(request, user)
            
            return redirect('index')
    
    return render(request, "registration/signup.html", {'form' : form, 'token' : token})

def signup_begin(request):
    context = RequestContext(request)
    
    if request.POST:
        form = VPNBeginSignupForm(request.POST)
    else:
        form = VPNBeginSignupForm()

    success = False
    
    if form.is_valid():
        token = get_random_string(length=50)
            
        invite = Invite(token=token, email=form.cleaned_data['email'])
        invite.save()
        
        url = request.build_absolute_uri(reverse('account_signup', args=[token]))
        
        message = render_to_string("account/signupmsg.txt", {'url' : url}, context_instance=context)
        
        send_branded_email("Inscription", message, form.cleaned_data['email'], context)
        
        success = True
        
    return render(request, "registration/begin.html", {'form' : form, 'success' : success})

def mailvalidation(request, token):
    try:
        validation = MailValidation.objects.get(token=token)
    except MailValidation.DoesNotExist:
        return render(request, 'account/mailvalidation.html', {'mail_success' : False})
    
    validation.user.email = validation.email
    validation.user.save()
    validation.delete()
    
    return render(request, 'account/mailvalidation.html', {'mail_success' : True})

def password_recovery_begin(request):
    context = RequestContext(request)
    
    success = False
    
    if not request.POST:
        form = PasswordRecoveryForm()
    else:
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid() and form.user:
            token = get_random_string(length=50)
            
            recovery = PasswordRecovery(user=form.user, email=form.cleaned_data['email'], token=token)
            recovery.save()
            
            url = request.build_absolute_uri(reverse('account_password_recovery', args=[token]))
            
            message = render_to_string("registration/recoverymsg.txt", {'url' : url}, context_instance=context)
            
            send_branded_email("Récupération de compte", message, form.cleaned_data['email'], context)
            
            success = True

    return render(request, 'registration/recovery_begin.html', {'form' : form, 'success' : success})

def password_recovery(request, token):
    try:
        recovery = PasswordRecovery.objects.get(token=token)
    except PasswordRecovery.DoesNotExist:
        return redirect('django.contrib.auth.views.login')
    
    if not request.POST:
        form = SetPasswordForm(recovery.user)
    else:
        form = SetPasswordForm(recovery.user, request.POST)
        
        if form.is_valid():
            form.save()
            recovery.delete()
    
    return render(request, 'registration/recovery.html', {'token' : token, 'form' : form, 'success' : form.is_valid()})
