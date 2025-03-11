from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    site_name = serializers.CharField(source='equipment.site.name', read_only=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'title', 'message', 'equipment', 'equipment_name', 'site_name', 'type', 'status', 'created_at', 'resolved_at']
        read_only_fields = ['id', 'created_at']
