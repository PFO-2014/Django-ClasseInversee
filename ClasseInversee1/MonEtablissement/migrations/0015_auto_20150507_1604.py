# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0014_auto_20150507_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messeance',
            name='ma_sequence',
        ),
        migrations.RemoveField(
            model_name='mesactivite',
            name='ma_seance',
        ),
        migrations.AddField(
            model_name='mesactivite',
            name='ma_sequence',
            field=models.ForeignKey(blank=True, to='MonEtablissement.MesSequence', null=True),
        ),
        migrations.DeleteModel(
            name='MesSeance',
        ),
    ]
