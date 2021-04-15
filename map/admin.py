from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass

@admin.register(Loc)
class LocAdmin(admin.ModelAdmin):
    pass
