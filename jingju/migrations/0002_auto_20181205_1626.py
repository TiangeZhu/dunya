# Generated by Django 2.1.2 on 2018-12-05 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jingju', '0001_squashed_0024_auto_20181205_0945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='alias',
            new_name='romanisation',
        ),
        migrations.AlterField(
            model_name='artist',
            name='role_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jingju.RoleType'),
        ),
        migrations.AlterField(
            model_name='roletype',
            name='code',
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='shengqiangbanshi',
            name='code',
            field=models.CharField(db_index=True, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='shengqiangbanshi',
            name='romanisation',
            field=models.CharField(max_length=100),
        ),
    ]
