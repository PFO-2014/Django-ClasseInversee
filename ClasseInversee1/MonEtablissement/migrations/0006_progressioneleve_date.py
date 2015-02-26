# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0005_remove_progressioneleve_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressioneleve',
            name='date',
            field=models.DateField(default=2015, verbose_name=b'date'),
            preserve_default=True,
        ),
    ]
