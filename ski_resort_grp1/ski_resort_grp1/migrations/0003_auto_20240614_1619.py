# Generated by Django 3.2.25 on 2024-06-14 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ski_resort_grp1', '0002_auto_20240614_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilift',
            name='travel_time',
        ),
        migrations.RemoveField(
            model_name='skiroute',
            name='length',
        ),
    ]
