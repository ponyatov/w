import config

from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin#,OSMGeoAdmin

from .models import *

# Register your models here.

@admin.register(Address)
class AddressAdmin(GeoModelAdmin):
    def addr(item): return f'{item}'
    addr.short_description = 'адрес'
    #
    list_display = [addr] + [
        field.name
        for field in Address._meta.get_fields()
        if field.name not in ['id']
    ]
    ordering = ['-area', 'city']

@admin.register(Area)
class AreaAdmin(GeoModelAdmin):
    default_lon = config.GIS_LON
    default_lat = config.GIS_LAT
    default_zoom = config.GIS_ZOOM

@admin.register(Loc)
class LocAdmin(GeoModelAdmin):
    default_lon = config.GIS_LON
    default_lat = config.GIS_LAT
    default_zoom = config.GIS_ZOOM
    ordering = ['-area', 'name']
