from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Dept)
class DeptAdmin(admin.ModelAdmin):
    pass # todo filter_horizontal

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Profile._meta.get_fields()
        if field.name not in ['id']
    ]
