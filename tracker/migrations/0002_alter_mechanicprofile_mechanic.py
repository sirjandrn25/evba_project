# Generated by Django 3.2.4 on 2021-06-17 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mechanicprofile',
            name='mechanic',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mechanic_profile', to='tracker.mechanic'),
        ),
    ]