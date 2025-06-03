from rest_framework import serializers
from .models import Site
from users.serializers import CompanySerializer


class SiteSerializer(serializers.ModelSerializer):
    """Serializer pour les sites."""
    company_name = serializers.CharField(source='company.name', read_only=True)
    equipment_count = serializers.SerializerMethodField()
    active_alerts_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Site
        fields = [
            'id', 'name', 'address', 'company', 'company_name', 
            'status', 'status_display', 'created_at', 'updated_at',
            'equipment_count', 'active_alerts_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_equipment_count(self, obj):
        """Retourne le nombre d'équipements sur ce site."""
        return obj.equipment.count()
    
    def get_active_alerts_count(self, obj):
        """Retourne le nombre d'alertes actives sur ce site."""
        return sum(equipment.alerts.filter(status='active').count() 
                  for equipment in obj.equipment.all())


class SiteCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création de sites."""
    
    class Meta:
        model = Site
        fields = ['name', 'address', 'company', 'status']
    
    def validate_name(self, value):
        """Valide l'unicité du nom de site dans l'entreprise."""
        company = self.initial_data.get('company')
        if company:
            existing = Site.objects.filter(
                company=company, 
                name=value
            ).exclude(pk=self.instance.pk if self.instance else None)
            if existing.exists():
                raise serializers.ValidationError(
                    "Un site avec ce nom existe déjà dans cette entreprise."
                )
        return value


class SiteUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour de sites."""
    
    class Meta:
        model = Site
        fields = ['name', 'address', 'status']
    
    def validate_name(self, value):
        """Valide l'unicité du nom de site dans l'entreprise."""
        if self.instance:
            existing = Site.objects.filter(
                company=self.instance.company, 
                name=value
            ).exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError(
                    "Un site avec ce nom existe déjà dans cette entreprise."
                )
        return value


class SiteDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les sites."""
    company_details = CompanySerializer(source='company', read_only=True)
    equipment_list = serializers.SerializerMethodField()
    equipment_count = serializers.SerializerMethodField()
    equipment_by_type = serializers.SerializerMethodField()
    equipment_by_status = serializers.SerializerMethodField()
    active_alerts_count = serializers.SerializerMethodField()
    recent_alerts = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Site
        fields = [
            'id', 'name', 'address', 'company', 'company_details',
            'status', 'status_display', 'created_at', 'updated_at',
            'equipment_count', 'equipment_list', 'equipment_by_type',
            'equipment_by_status', 'active_alerts_count', 'recent_alerts'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_equipment_list(self, obj):
        """Retourne la liste des équipements."""
        from equipment.serializers import EquipmentSerializer
        equipment = obj.equipment.all()
        return EquipmentSerializer(equipment, many=True).data
    
    def get_equipment_count(self, obj):
        """Retourne le nombre d'équipements."""
        return obj.equipment.count()
    
    def get_equipment_by_type(self, obj):
        """Retourne la répartition des équipements par type."""
        from django.db.models import Count
        return dict(
            obj.equipment.values('type')
            .annotate(count=Count('type'))
            .values_list('type', 'count')
        )
    
    def get_equipment_by_status(self, obj):
        """Retourne la répartition des équipements par statut."""
        from django.db.models import Count
        return dict(
            obj.equipment.values('status')
            .annotate(count=Count('status'))
            .values_list('status', 'count')
        )
    
    def get_active_alerts_count(self, obj):
        """Retourne le nombre d'alertes actives."""
        return sum(equipment.alerts.filter(status='active').count() 
                  for equipment in obj.equipment.all())
    
    def get_recent_alerts(self, obj):
        """Retourne les 10 dernières alertes du site."""
        from alerts.serializers import AlertSerializer
        from alerts.models import Alert
        
        recent_alerts = Alert.objects.filter(
            equipment__site=obj
        ).order_by('-created_at')[:10]
        
        return AlertSerializer(recent_alerts, many=True).data


class SiteStatsSerializer(serializers.Serializer):
    """Serializer pour les statistiques de sites."""
    total_sites = serializers.IntegerField()
    online_sites = serializers.IntegerField()
    offline_sites = serializers.IntegerField()
    warning_sites = serializers.IntegerField()
    pending_sites = serializers.IntegerField()
    sites_by_company = serializers.DictField()
    average_equipment_per_site = serializers.FloatField()


class SiteBulkUpdateSerializer(serializers.Serializer):
    """Serializer pour la mise à jour en lot de sites."""
    site_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    status = serializers.ChoiceField(
        choices=Site.STATUS_CHOICES,
        required=False
    )
    
    def validate_site_ids(self, value):
        """Valide que tous les sites existent."""
        existing_sites = Site.objects.filter(id__in=value).count()
        if existing_sites != len(value):
            raise serializers.ValidationError("Certains sites n'existent pas.")
        return value
