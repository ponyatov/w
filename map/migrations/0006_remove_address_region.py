# Generated by Django 3.2 on 2021-04-19 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_alter_address_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='region',
        ),
    ]