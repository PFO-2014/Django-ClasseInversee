# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('MonEtablissement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=250, verbose_name=b'description')),
                ('sequence_f', models.ForeignKey(blank=True, to='MonEtablissement.MesSequence', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domaine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(unique=True, max_length=50)),
                ('color', models.CharField(default=b'#cdcdcd', unique=True, max_length=7)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='progressioneleve',
            name='date',
            field=models.DateField(null=True,verbose_name=b'date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eleve',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mesclasse',
            name='annee_cours_dateint',
            field=models.IntegerField(default=2015, verbose_name=b'Ann\xc3\xa9e en cours'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='messequence',
            name='domaine',
            field=models.ForeignKey(blank=True, to='MonEtablissement.Domaine', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='messequence',
            name='full_description_sequence',
            field=models.TextField(null=True, verbose_name=b"Description d'une s\xc3\xa9quence", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progressioneleve',
            name='activite',
            field=models.ForeignKey(blank=True, to='MonEtablissement.MesActivite', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progressioneleve',
            name='eleve',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progressioneleve',
            name='resultat',
            field=models.IntegerField(null=True, verbose_name=b'Note', blank=True),
            preserve_default=True,
        ),
    ]
