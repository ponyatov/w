# Generated by Django 3.2 on 2021-04-17 04:30

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20210415_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='loc',
            name='area',
            field=django.contrib.gis.db.models.fields.PolygonField(
                blank=True, null=True, srid=4326),
        ),
    ]
