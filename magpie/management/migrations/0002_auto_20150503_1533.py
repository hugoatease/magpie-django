# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionlog',
            name='origin',
            field=models.GenericIPAddressField(protocol=b'IPv4'),
        ),
        migrations.AlterField(
            model_name='userconfig',
            name='current_origin',
            field=models.GenericIPAddressField(null=True, protocol=b'IPv4', blank=True),
        ),
    ]
