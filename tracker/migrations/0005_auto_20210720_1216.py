# Generated by Django 3.2.4 on 2021-07-20 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_driverprofile_is_busy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help', to='tracker.driver'),
        ),
        migrations.AlterField(
            model_name='help',
            name='mechanic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help', to='tracker.mechanic'),
        ),
    ]
