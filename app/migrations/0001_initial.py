# Generated by Django 3.2 on 2021-04-17 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=34, verbose_name='приложение')),
                ('url', models.URLField(verbose_name='стартовая ссылка')),
            ],
            options={
                'verbose_name': 'приложение',
                'verbose_name_plural': 'приложения',
            },
        ),
    ]
