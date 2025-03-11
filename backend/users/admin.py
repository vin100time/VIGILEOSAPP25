from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'company', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('company', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('company', 'phone')}),
    )
    list_filter = UserAdmin.list_filter + ('company',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
