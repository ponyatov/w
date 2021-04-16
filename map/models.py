from django.contrib.gis.db import models

# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=0x22, verbose_name='регион')
    area = models.PolygonField(blank=True, null=True)

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'

    def __str__(self): return f'{self.name}'

## geoLocation
class Loc(models.Model):
    name = models.CharField(max_length=0x22, verbose_name='локация')
    loc = models.PointField(blank=True, null=True)

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self): return f'{self.name}'
