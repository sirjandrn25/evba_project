# Generated by Django 3.2.4 on 2021-06-20 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('license_no', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mechanic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('pan_no', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='service/')),
            ],
        ),
        migrations.CreateModel(
            name='MechanicProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_name', models.CharField(blank=True, max_length=150)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('is_approve', models.BooleanField(default=False)),
                ('contact_no', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=False)),
                ('is_busy', models.BooleanField(default=False)),
                ('mechanic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mechanic_profile', to='tracker.mechanic')),
                ('services', models.ManyToManyField(to='tracker.Service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_accept', models.BooleanField(default=False)),
                ('vehicle_type', models.CharField(choices=[('two_wheeler', 'Two wheeler'), ('four_wheeler', 'Four Wheeler')], default='two_wheeler', max_length=20)),
                ('problem_desc', models.TextField(blank=True)),
                ('curr_driver_lat', models.FloatField()),
                ('curr_driver_long', models.FloatField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_driver', to='tracker.driver')),
                ('mechanic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_mechanic', to='tracker.mechanic')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DriverProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('is_approve', models.BooleanField(default=False)),
                ('contact_no', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=150)),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='tracker.driver')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]