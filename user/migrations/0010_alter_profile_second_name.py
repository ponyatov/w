# Generated by Django 3.2 on 2021-04-19 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20210419_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='second_name',
            field=models.CharField(
                blank=True, max_length=34, null=True, verbose_name='отчество'),
        ),
    ]
