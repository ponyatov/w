# Generated by Django 3.2 on 2021-04-19 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210419_0905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'verbose_name': 'должность',
                     'verbose_name_plural': 'должности'},
        ),
        migrations.AlterField(
            model_name='position',
            name='grade',
            field=models.CharField(
                blank=True, max_length=51, null=True, verbose_name='грейд (категория)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='user.position', verbose_name='должность'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='room',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.room', verbose_name='комната'),
        ),
    ]
