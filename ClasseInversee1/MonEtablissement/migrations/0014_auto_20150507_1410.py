# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0013_progressioneleve_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressioneleve',
            name='eleve',
            field=models.ForeignKey(to='MonEtablissement.Eleve'),
        ),
    ]
