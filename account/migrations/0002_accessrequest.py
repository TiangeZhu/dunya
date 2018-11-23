# Generated by Django 2.1.2 on 2018-11-13 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('justification', models.TextField()),
                ('approved', models.BooleanField(null=True)),
                ('processeddate', models.DateTimeField(blank=True, null=True)),
                ('processedby', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access_request_approvals', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['requestdate'],
            },
        ),
    ]