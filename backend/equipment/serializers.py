from rest_framework import serializers
from .models import Equipment
from sites.serializers import SiteSerializer

class EquipmentSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='site.name', read_only=True)
    
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'site', 'site_name', 'status', 'ip_address', 'last_maintenance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
