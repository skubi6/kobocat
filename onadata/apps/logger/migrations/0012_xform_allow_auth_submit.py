# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0011_add-index-to-instance-uuid_and_xform_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='xform',
            name='allow_auth_submit',
            field=models.BooleanField(default=False),
        ),
    ]
