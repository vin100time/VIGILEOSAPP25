from rest_framework import serializers
from django.utils import timezone
from .models import Equipment
from sites.serializers import SiteSerializer


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer pour les équipements."""
    site_name = serializers.CharField(source='site.name', read_only=True)
    site_address = serializers.CharField(source='site.address', read_only=True)
    company_name = serializers.CharField(source='site.company.name', read_only=True)
    alerts_count = serializers.SerializerMethodField()
    active_alerts_count = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_since_maintenance = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'type', 'type_display', 'site', 'site_name', 
            'site_address', 'company_name', 'status', 'status_display',
            'ip_address', 'last_maintenance', 'days_since_maintenance',
            'created_at', 'updated_at', 'alerts_count', 'active_alerts_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_alerts_count(self, obj):
        """Retourne le nombre total d'alertes pour cet équipement."""
        return obj.alerts.count()
    
    def get_active_alerts_count(self, obj):
        """Retourne le nombre d'alertes actives pour cet équipement."""
        return obj.alerts.filter(status='active').count()
    
    def get_days_since_maintenance(self, obj):
        """Calcule le nombre de jours depuis la dernière maintenance."""
        if obj.last_maintenance:
            return (timezone.now().date() - obj.last_maintenance).days
        return None


class EquipmentCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'équipements."""
    
    class Meta:
        model = Equipment
        fields = [
            'name', 'type', 'site', 'status', 'ip_address', 'last_maintenance'
        ]
    
    def validate_ip_address(self, value):
        """Valide l'unicité de l'adresse IP dans le site."""
        if value:
            site = self.initial_data.get('site')
            if site:
                existing = Equipment.objects.filter(
                    site=site, 
                    ip_address=value
                ).exclude(pk=self.instance.pk if self.instance else None)
                if existing.exists():
                    raise serializers.ValidationError(
                        "Cette adresse IP est déjà utilisée sur ce site."
                    )
        return value


class EquipmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour d'équipements."""
    
    class Meta:
        model = Equipment
        fields = [
            'name', 'type', 'status', 'ip_address', 'last_maintenance'
        ]
    
    def validate_ip_address(self, value):
        """Valide l'unicité de l'adresse IP dans le site."""
        if value and self.instance:
            existing = Equipment.objects.filter(
                site=self.instance.site, 
                ip_address=value
            ).exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError(
                    "Cette adresse IP est déjà utilisée sur ce site."
                )
        return value


class EquipmentDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les équipements."""
    site_details = SiteSerializer(source='site', read_only=True)
    recent_alerts = serializers.SerializerMethodField()
    alerts_count = serializers.SerializerMethodField()
    active_alerts_count = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_since_maintenance = serializers.SerializerMethodField()
    maintenance_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'type', 'type_display', 'site', 'site_details',
            'status', 'status_display', 'ip_address', 'last_maintenance',
            'days_since_maintenance', 'maintenance_status', 'created_at', 
            'updated_at', 'alerts_count', 'active_alerts_count', 'recent_alerts'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_recent_alerts(self, obj):
        """Retourne les 5 dernières alertes."""
        from alerts.serializers import AlertSerializer
        recent_alerts = obj.alerts.order_by('-created_at')[:5]
        return AlertSerializer(recent_alerts, many=True).data
    
    def get_alerts_count(self, obj):
        """Retourne le nombre total d'alertes."""
        return obj.alerts.count()
    
    def get_active_alerts_count(self, obj):
        """Retourne le nombre d'alertes actives."""
        return obj.alerts.filter(status='active').count()
    
    def get_days_since_maintenance(self, obj):
        """Calcule le nombre de jours depuis la dernière maintenance."""
        if obj.last_maintenance:
            return (timezone.now().date() - obj.last_maintenance).days
        return None
    
    def get_maintenance_status(self, obj):
        """Détermine le statut de maintenance."""
        if not obj.last_maintenance:
            return 'unknown'
        
        days = (timezone.now().date() - obj.last_maintenance).days
        if days > 365:
            return 'overdue'
        elif days > 300:
            return 'due_soon'
        else:
            return 'ok'


class EquipmentStatsSerializer(serializers.Serializer):
    """Serializer pour les statistiques d'équipements."""
    total_equipment = serializers.IntegerField()
    online_equipment = serializers.IntegerField()
    offline_equipment = serializers.IntegerField()
    warning_equipment = serializers.IntegerField()
    equipment_by_type = serializers.DictField()
    equipment_by_site = serializers.DictField()
    maintenance_overdue = serializers.IntegerField()


class EquipmentMaintenanceSerializer(serializers.Serializer):
    """Serializer pour la maintenance d'équipements."""
    equipment_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    maintenance_date = serializers.DateField(default=timezone.now().date())
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_equipment_ids(self, value):
        """Valide que tous les équipements existent."""
        existing_equipment = Equipment.objects.filter(id__in=value).count()
        if existing_equipment != len(value):
            raise serializers.ValidationError("Certains équipements n'existent pas.")
        return value
    
    def validate_maintenance_date(self, value):
        """Valide que la date de maintenance n'est pas dans le futur."""
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "La date de maintenance ne peut pas être dans le futur."
            )
        return value


class EquipmentBulkUpdateSerializer(serializers.Serializer):
    """Serializer pour la mise à jour en lot d'équipements."""
    equipment_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    status = serializers.ChoiceField(
        choices=Equipment.STATUS_CHOICES,
        required=False
    )
    last_maintenance = serializers.DateField(required=False)
    
    def validate_equipment_ids(self, value):
        """Valide que tous les équipements existent."""
        existing_equipment = Equipment.objects.filter(id__in=value).count()
        if existing_equipment != len(value):
            raise serializers.ValidationError("Certains équipements n'existent pas.")
        return value
