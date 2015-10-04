# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0002_auto_20151004_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='segment_id',
            new_name='segment',
        ),
    ]
