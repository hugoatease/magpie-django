# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=75)),
                ('token', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Invitation',
                'verbose_name_plural': 'Invitations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailValidation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=75)),
                ('token', models.CharField(max_length=64)),
                ('user', models.ForeignKey(related_name='mailvalidations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "Validation d'addresse e-mail",
                'verbose_name_plural': "Validations d'addresse e-mail",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=75)),
                ('token', models.CharField(max_length=64)),
                ('user', models.ForeignKey(related_name='passwordrecoveries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
