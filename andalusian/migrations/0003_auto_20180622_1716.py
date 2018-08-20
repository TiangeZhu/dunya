# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-22 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('andalusian', '0002_auto_20161006_1700'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='form',
            options={'ordering': ['display_order', 'id']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='instrument',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='mizan',
            options={'ordering': ['display_order', 'id']},
        ),
        migrations.AlterModelOptions(
            name='nawba',
            options={'ordering': ['display_order', 'id']},
        ),
        migrations.AlterModelOptions(
            name='orchestra',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='poem',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='recording',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='sanaa',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='tab',
            options={'ordering': ['display_order', 'id']},
        ),
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='form',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='form',
            name='uuid',
            field=models.UUIDField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='mizan',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mizan',
            name='uuid',
            field=models.UUIDField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='nawba',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nawba',
            name='uuid',
            field=models.UUIDField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='tab',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tab',
            name='uuid',
            field=models.UUIDField(db_index=True, null=True),
        ),
    ]