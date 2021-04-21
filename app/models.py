from django.db import models

# Create your models here.

class App(models.Model):
    name = models.CharField('приложение', max_length=0x11)
    title = models.CharField(
        'описание', max_length=0x33, blank=True, null=True)

    class Meta:
        verbose_name = 'приложение'
        verbose_name_plural = 'приложения'

    def __str__(self): return f'{self.name}'
