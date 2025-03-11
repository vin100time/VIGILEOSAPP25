from django.contrib import admin
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'site', 'status', 'ip_address')
    list_filter = ('type', 'status', 'site__company')
    search_fields = ('name', 'ip_address')
