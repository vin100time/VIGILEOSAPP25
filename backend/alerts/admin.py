from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'equipment', 'type', 'status', 'created_at')
    list_filter = ('type', 'status', 'equipment__site__company')
    search_fields = ('title', 'message')
