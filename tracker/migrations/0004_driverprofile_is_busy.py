# Generated by Django 3.2.4 on 2021-06-23 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_alter_driverprofile_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverprofile',
            name='is_busy',
            field=models.BooleanField(default=False),
        ),
    ]
