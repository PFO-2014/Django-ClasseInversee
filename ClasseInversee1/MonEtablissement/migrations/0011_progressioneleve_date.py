# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0010_remove_progressioneleve_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressioneleve',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date', null=True),
            preserve_default=True,
        ),
    ]
