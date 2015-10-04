# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('translation', models.TextField(max_length=2000)),
                ('reference', models.TextField(max_length=2000)),
                ('batch_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='rating',
            name='segment_id',
            field=models.ForeignKey(to='rater.Segment'),
        ),
    ]
