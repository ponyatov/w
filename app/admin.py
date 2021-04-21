from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in App._meta.get_fields()
        if field.name not in ['id']
    ]
    ordering = ['id']
