# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-06 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
        ('makam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='references',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='source',
        ),
        migrations.RemoveField(
            model_name='composer',
            name='references',
        ),
        migrations.RemoveField(
            model_name='composer',
            name='source',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='references',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='source',
        ),
        migrations.RemoveField(
            model_name='recording',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recording',
            name='references',
        ),
        migrations.RemoveField(
            model_name='recording',
            name='source',
        ),
        migrations.RemoveField(
            model_name='release',
            name='description',
        ),
        migrations.RemoveField(
            model_name='release',
            name='references',
        ),
        migrations.RemoveField(
            model_name='release',
            name='source',
        ),
        migrations.RemoveField(
            model_name='work',
            name='description',
        ),
        migrations.RemoveField(
            model_name='work',
            name='references',
        ),
        migrations.RemoveField(
            model_name='work',
            name='source',
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makam_artist_image', to='data.Image'),
        ),
        migrations.AddField(
            model_name='composer',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makam_composer_image', to='data.Image'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makam_instrument_image', to='data.Image'),
        ),
        migrations.AddField(
            model_name='release',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makam_release_image', to='data.Image'),
        ),
    ]
