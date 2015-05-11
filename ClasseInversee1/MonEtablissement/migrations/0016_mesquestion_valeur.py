# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0015_auto_20150507_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesquestion',
            name='valeur',
            field=models.IntegerField(default=1),
        ),
    ]
