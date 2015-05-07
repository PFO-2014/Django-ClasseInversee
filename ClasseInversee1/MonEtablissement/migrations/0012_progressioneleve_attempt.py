# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0011_progressioneleve_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressioneleve',
            name='attempt',
            field=models.IntegerField(default=1, verbose_name=b'attempt'),
        ),
    ]
