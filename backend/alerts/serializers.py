from rest_framework import serializers
from django.utils import timezone
from .models import Alert
from equipment.serializers import EquipmentSerializer


class AlertSerializer(serializers.ModelSerializer):
    """Serializer pour les alertes."""
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    equipment_type = serializers.CharField(source='equipment.type', read_only=True)
    site_name = serializers.CharField(source='equipment.site.name', read_only=True)
    site_id = serializers.IntegerField(source='equipment.site.id', read_only=True)
    company_name = serializers.CharField(source='equipment.site.company.name', read_only=True)
    duration = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'title', 'message', 'equipment', 'equipment_name', 
            'equipment_type', 'site_name', 'site_id', 'company_name',
            'type', 'status', 'created_at', 'resolved_at', 'duration', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_duration(self, obj):
        """Calcule la durée de l'alerte."""
        if obj.resolved_at:
            return (obj.resolved_at - obj.created_at).total_seconds()
        else:
            return (timezone.now() - obj.created_at).total_seconds()
    
    def get_is_active(self, obj):
        """Indique si l'alerte est active."""
        return obj.status == 'active'


class AlertCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'alertes."""
    
    class Meta:
        model = Alert
        fields = ['title', 'message', 'equipment', 'type']
    
    def create(self, validated_data):
        """Crée une nouvelle alerte."""
        validated_data['status'] = 'active'
        return super().create(validated_data)


class AlertUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour d'alertes."""
    
    class Meta:
        model = Alert
        fields = ['title', 'message', 'type', 'status']
    
    def update(self, instance, validated_data):
        """Met à jour une alerte."""
        # Si le statut passe à 'resolved', on met la date de résolution
        if validated_data.get('status') == 'resolved' and instance.status != 'resolved':
            validated_data['resolved_at'] = timezone.now()
        
        # Si le statut repasse à 'active', on supprime la date de résolution
        if validated_data.get('status') == 'active' and instance.status == 'resolved':
            validated_data['resolved_at'] = None
        
        return super().update(instance, validated_data)


class AlertDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les alertes."""
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)
    duration = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Alert
        fields = [
            'id', 'title', 'message', 'equipment', 'equipment_details',
            'type', 'type_display', 'status', 'status_display',
            'created_at', 'resolved_at', 'duration', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_duration(self, obj):
        """Calcule la durée de l'alerte."""
        if obj.resolved_at:
            return (obj.resolved_at - obj.created_at).total_seconds()
        else:
            return (timezone.now() - obj.created_at).total_seconds()
    
    def get_is_active(self, obj):
        """Indique si l'alerte est active."""
        return obj.status == 'active'


class AlertStatsSerializer(serializers.Serializer):
    """Serializer pour les statistiques d'alertes."""
    total_alerts = serializers.IntegerField()
    active_alerts = serializers.IntegerField()
    acknowledged_alerts = serializers.IntegerField()
    resolved_alerts = serializers.IntegerField()
    alerts_by_type = serializers.DictField()
    alerts_by_site = serializers.DictField()
    average_resolution_time = serializers.FloatField()


class AlertAcknowledgeSerializer(serializers.Serializer):
    """Serializer pour l'accusé de réception d'alertes."""
    alert_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    
    def validate_alert_ids(self, value):
        """Valide que toutes les alertes existent."""
        existing_alerts = Alert.objects.filter(id__in=value).count()
        if existing_alerts != len(value):
            raise serializers.ValidationError("Certaines alertes n'existent pas.")
        return value


class AlertResolveSerializer(serializers.Serializer):
    """Serializer pour la résolution d'alertes."""
    alert_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    resolution_message = serializers.CharField(required=False, allow_blank=True)
    
    def validate_alert_ids(self, value):
        """Valide que toutes les alertes existent."""
        existing_alerts = Alert.objects.filter(id__in=value).count()
        if existing_alerts != len(value):
            raise serializers.ValidationError("Certaines alertes n'existent pas.")
        return value
