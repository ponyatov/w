# Generated by Django 3.2 on 2021-04-19 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0009_auto_20210419_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='loc',
            name='area',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='map.area', verbose_name='регион'),
        ),
    ]