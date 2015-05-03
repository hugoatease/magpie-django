# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.GenericIPAddressField(protocol=b'IPv4'),
        ),
        migrations.AlterField(
            model_name='server',
            name='address',
            field=models.GenericIPAddressField(protocol=b'IPv4'),
        ),
        migrations.AlterField(
            model_name='subnet',
            name='address',
            field=models.GenericIPAddressField(protocol=b'IPv4'),
        ),
    ]
