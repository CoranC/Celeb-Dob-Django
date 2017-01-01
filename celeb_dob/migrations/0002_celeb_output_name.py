# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celeb_dob', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='celeb',
            name='output_name',
            field=models.CharField(default=b'', max_length=128),
            preserve_default=True,
        ),
    ]
