# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0004_progressioneleve_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressioneleve',
            name='date',
        ),
    ]
