from django.contrib.gis.db import models

# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=0x22, verbose_name='регион')
    code = models.IntegerField('код', blank=True, null=True)
    area = models.PolygonField(blank=True, null=True)

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'

    def __str__(self):
        code = f'{self.code}: ' if self.code else ''
        return f'{code}{self.name}'

## geoLocation
class Loc(models.Model):
    name = models.CharField(max_length=0x22, verbose_name='локация')
    okato = models.CharField('ОКАТО', max_length=0x22, blank=True, null=True)
    area = models.ForeignKey(Area, verbose_name='регион',
                             on_delete=models.DO_NOTHING, null=True)
    bounds = models.PolygonField(
        blank=True, verbose_name='границы территории', null=True)
    loc = models.PointField(
        blank=True, verbose_name='географический центр', null=True)

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self): return f'{self.name}'

class Address(models.Model):
    zip = models.IntegerField('почтовый индекс')
    area = models.ForeignKey(
        Area, verbose_name='регион', on_delete=models.DO_NOTHING, null=True)
    city = models.CharField('населённый пункт', max_length=0x22)
    street = models.CharField('улица', max_length=0x55)
    house = models.CharField('дом', max_length=5)

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    def __str__(self): return f'{self.city} {self.street} {self.house}'
