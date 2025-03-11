from django.contrib import admin
from .models import Site

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'status', 'created_at')
    list_filter = ('status', 'company')
    search_fields = ('name', 'address')
