# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0012_progressioneleve_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressioneleve',
            name='question',
            field=models.TextField(null=True, verbose_name=b'Question \xc3\xa9l\xc3\xa8ve ', blank=True),
        ),
    ]
