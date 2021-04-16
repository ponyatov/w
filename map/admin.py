from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import *

# Register your models here.

@admin.register(Area)
class AreaAdmin(OSMGeoAdmin):
    pass

@admin.register(Loc)
class LocAdmin(OSMGeoAdmin):
    pass
