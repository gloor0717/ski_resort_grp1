# Generated by Django 3.2.25 on 2024-06-16 18:14

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ski_resort_grp1', '0006_basestation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skiroute',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=4326),
        ),
    ]
