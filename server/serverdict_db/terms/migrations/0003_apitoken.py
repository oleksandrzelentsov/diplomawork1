# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('terms', '0002_term_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIToken',
            fields=[
                ('token', models.TextField(serialize=False, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
    ]
