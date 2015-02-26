# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0006_progressioneleve_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressioneleve',
            name='date',
            field=models.DateField(null=True, verbose_name=b'date', blank=True),
            preserve_default=True,
        ),
    ]
