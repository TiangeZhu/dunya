# Generated by Django 2.1.2 on 2019-01-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('andalusian', '0003_auto_20180622_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
    ]