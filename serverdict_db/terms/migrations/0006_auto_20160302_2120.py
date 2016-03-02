# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0005_auto_20160214_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2016, 3, 2, 19, 20, 0, 922964, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='term',
            name='accesibility',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='granted_users', blank=True),
        ),
    ]
