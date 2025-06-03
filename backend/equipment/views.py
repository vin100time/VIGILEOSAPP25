from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Equipment
from .serializers import (
    EquipmentSerializer, EquipmentCreateSerializer, EquipmentUpdateSerializer,
    EquipmentDetailSerializer, EquipmentStatsSerializer, EquipmentMaintenanceSerializer,
    EquipmentBulkUpdateSerializer
)


class EquipmentViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des équipements."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'site', 'site__company']
    search_fields = ['name', 'ip_address', 'site__name', 'site__address']
    ordering_fields = ['name', 'created_at', 'updated_at', 'last_maintenance', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtre les équipements selon les permissions de l'utilisateur."""
        user = self.request.user
        
        if user.is_staff:
            queryset = Equipment.objects.all()
        elif user.company:
            queryset = Equipment.objects.filter(site__company=user.company)
        else:
            queryset = Equipment.objects.none()
        
        # Filtres supplémentaires via query params
        site_id = self.request.query_params.get('site')
        if site_id:
            try:
                queryset = queryset.filter(site_id=int(site_id))
            except ValueError:
                pass
        
        # Filtrer par statut de maintenance
        maintenance_status = self.request.query_params.get('maintenance_status')
        if maintenance_status == 'overdue':
            # Équipements sans maintenance depuis plus d'un an
            one_year_ago = timezone.now().date() - timedelta(days=365)
            queryset = queryset.filter(
                Q(last_maintenance__lt=one_year_ago) | Q(last_maintenance__isnull=True)
            )
        elif maintenance_status == 'due_soon':
            # Équipements avec maintenance due dans les 2 mois
            ten_months_ago = timezone.now().date() - timedelta(days=300)
            one_year_ago = timezone.now().date() - timedelta(days=365)
            queryset = queryset.filter(
                last_maintenance__lt=ten_months_ago,
                last_maintenance__gte=one_year_ago
            )
        
        return queryset.select_related('site', 'site__company')
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action."""
        if self.action == 'create':
            return EquipmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EquipmentUpdateSerializer
        elif self.action == 'retrieve':
            return EquipmentDetailSerializer
        return EquipmentSerializer
    
    def perform_create(self, serializer):
        """Personnalise la création d'équipement."""
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        """Récupère les alertes d'un équipement."""
        equipment = self.get_object()
        alerts = equipment.alerts.all().order_by('-created_at')
        
        # Filtrer par statut si spécifié
        status_filter = request.query_params.get('status')
        if status_filter:
            alerts = alerts.filter(status=status_filter)
        
        # Limiter le nombre de résultats
        limit = int(request.query_params.get('limit', 20))
        alerts = alerts[:limit]
        
        from alerts.serializers import AlertSerializer
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        """Récupère les métriques récentes d'un équipement."""
        equipment = self.get_object()
        
        # Période par défaut : dernières 24h
        hours = int(request.query_params.get('hours', 24))
        start_time = timezone.now() - timedelta(hours=hours)
        
        # Vérifier si l'app metrics existe
        try:
            from metrics.models import NetworkMetric
            from metrics.serializers import NetworkMetricSerializer
            
            metrics = NetworkMetric.objects.filter(
                equipment=equipment,
                timestamp__gte=start_time
            ).order_by('-timestamp')
            
            limit = int(request.query_params.get('limit', 100))
            metrics = metrics[:limit]
            
            serializer = NetworkMetricSerializer(metrics, many=True)
            return Response(serializer.data)
        except ImportError:
            return Response({
                'message': 'Module de métriques non disponible',
                'metrics': []
            })
    
    @action(detail=True, methods=['post'])
    def set_maintenance(self, request, pk=None):
        """Met un équipement en maintenance."""
        equipment = self.get_object()
        maintenance_date = request.data.get('maintenance_date', timezone.now().date())
        notes = request.data.get('notes', '')
        
        if isinstance(maintenance_date, str):
            from datetime import datetime
            maintenance_date = datetime.strptime(maintenance_date, '%Y-%m-%d').date()
        
        equipment.last_maintenance = maintenance_date
        equipment.save()
        
        return Response({
            'message': 'Maintenance enregistrée',
            'maintenance_date': maintenance_date,
            'notes': notes
        })
    
    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        """Change le statut d'un équipement."""
        equipment = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in [choice[0] for choice in Equipment.STATUS_CHOICES]:
            return Response(
                {'error': 'Statut invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = equipment.status
        equipment.status = new_status
        equipment.save()
        
        return Response({
            'message': f'Statut changé de {old_status} à {new_status}',
            'old_status': old_status,
            'new_status': new_status
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des équipements."""
        queryset = self.get_queryset()
        
        # Statistiques générales
        total_equipment = queryset.count()
        online_equipment = queryset.filter(status='online').count()
        offline_equipment = queryset.filter(status='offline').count()
        warning_equipment = queryset.filter(status='warning').count()
        
        # Équipements par type
        equipment_by_type = dict(
            queryset.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )
        
        # Équipements par site
        equipment_by_site = dict(
            queryset.values('site__name')
            .annotate(count=Count('id'))
            .values_list('site__name', 'count')
        )
        
        # Maintenance en retard
        one_year_ago = timezone.now().date() - timedelta(days=365)
        maintenance_overdue = queryset.filter(
            Q(last_maintenance__lt=one_year_ago) | Q(last_maintenance__isnull=True)
        ).count()
        
        stats_data = {
            'total_equipment': total_equipment,
            'online_equipment': online_equipment,
            'offline_equipment': offline_equipment,
            'warning_equipment': warning_equipment,
            'equipment_by_type': equipment_by_type,
            'equipment_by_site': equipment_by_site,
            'maintenance_overdue': maintenance_overdue
        }
        
        serializer = EquipmentStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def maintenance_due(self, request):
        """Équipements nécessitant une maintenance."""
        queryset = self.get_queryset()
        
        # Équipements sans maintenance depuis plus d'un an
        one_year_ago = timezone.now().date() - timedelta(days=365)
        overdue = queryset.filter(
            Q(last_maintenance__lt=one_year_ago) | Q(last_maintenance__isnull=True)
        )
        
        # Équipements avec maintenance due bientôt (plus de 10 mois)
        ten_months_ago = timezone.now().date() - timedelta(days=300)
        due_soon = queryset.filter(
            last_maintenance__lt=ten_months_ago,
            last_maintenance__gte=one_year_ago
        )
        
        return Response({
            'overdue': EquipmentSerializer(overdue, many=True).data,
            'due_soon': EquipmentSerializer(due_soon, many=True).data,
            'overdue_count': overdue.count(),
            'due_soon_count': due_soon.count()
        })
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Équipements groupés par statut."""
        queryset = self.get_queryset()
        status_filter = request.query_params.get('status')
        
        if status_filter:
            equipment = queryset.filter(status=status_filter)
            page = self.paginate_queryset(equipment)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(equipment, many=True)
            return Response(serializer.data)
        
        # Retourner tous les statuts
        result = {}
        for status_choice in Equipment.STATUS_CHOICES:
            status_code = status_choice[0]
            equipment = queryset.filter(status=status_code)
            result[status_code] = {
                'count': equipment.count(),
                'equipment': EquipmentSerializer(equipment[:10], many=True).data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Équipements groupés par type."""
        queryset = self.get_queryset()
        type_filter = request.query_params.get('type')
        
        if type_filter:
            equipment = queryset.filter(type=type_filter)
            page = self.paginate_queryset(equipment)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(equipment, many=True)
            return Response(serializer.data)
        
        # Retourner tous les types
        result = {}
        for type_choice in Equipment.TYPE_CHOICES:
            type_code = type_choice[0]
            equipment = queryset.filter(type=type_code)
            result[type_code] = {
                'count': equipment.count(),
                'equipment': EquipmentSerializer(equipment[:10], many=True).data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def bulk_maintenance(self, request):
        """Enregistre la maintenance pour plusieurs équipements."""
        serializer = EquipmentMaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            equipment_ids = serializer.validated_data['equipment_ids']
            maintenance_date = serializer.validated_data['maintenance_date']
            notes = serializer.validated_data.get('notes', '')
            
            equipment = self.get_queryset().filter(id__in=equipment_ids)
            updated_count = equipment.update(last_maintenance=maintenance_date)
            
            return Response({
                'message': f'Maintenance enregistrée pour {updated_count} équipements',
                'maintenance_date': maintenance_date,
                'notes': notes
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Met à jour plusieurs équipements en masse."""
        serializer = EquipmentBulkUpdateSerializer(data=request.data)
        if serializer.is_valid():
            equipment_ids = serializer.validated_data['equipment_ids']
            update_data = {}
            
            if 'status' in serializer.validated_data:
                update_data['status'] = serializer.validated_data['status']
            
            if 'last_maintenance' in serializer.validated_data:
                update_data['last_maintenance'] = serializer.validated_data['last_maintenance']
            
            if update_data:
                equipment = self.get_queryset().filter(id__in=equipment_ids)
                updated_count = equipment.update(**update_data)
                
                return Response({
                    'message': f'{updated_count} équipements mis à jour',
                    'updated_fields': list(update_data.keys())
                })
            else:
                return Response(
                    {'error': 'Aucun champ à mettre à jour'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Données pour le tableau de bord des équipements."""
        queryset = self.get_queryset()
        
        # Statistiques générales
        total = queryset.count()
        online = queryset.filter(status='online').count()
        offline = queryset.filter(status='offline').count()
        warning = queryset.filter(status='warning').count()
        
        # Maintenance
        one_year_ago = timezone.now().date() - timedelta(days=365)
        ten_months_ago = timezone.now().date() - timedelta(days=300)
        
        maintenance_overdue = queryset.filter(
            Q(last_maintenance__lt=one_year_ago) | Q(last_maintenance__isnull=True)
        ).count()
        
        maintenance_due_soon = queryset.filter(
            last_maintenance__lt=ten_months_ago,
            last_maintenance__gte=one_year_ago
        ).count()
        
        # Répartition par type
        equipment_by_type = dict(
            queryset.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )
        
        # Équipements récemment ajoutés
        recent_equipment = queryset.order_by('-created_at')[:5]
        
        # Équipements avec le plus d'alertes actives
        equipment_with_alerts = []
        for eq in queryset.annotate(
            active_alerts=Count('alerts', filter=Q(alerts__status='active'))
        ).filter(active_alerts__gt=0).order_by('-active_alerts')[:5]:
            equipment_with_alerts.append({
                'id': eq.id,
                'name': eq.name,
                'site_name': eq.site.name,
                'active_alerts': eq.active_alerts
            })
        
        dashboard_data = {
            'summary': {
                'total': total,
                'online': online,
                'offline': offline,
                'warning': warning,
                'maintenance_overdue': maintenance_overdue,
                'maintenance_due_soon': maintenance_due_soon
            },
            'equipment_by_type': equipment_by_type,
            'recent_equipment': EquipmentSerializer(recent_equipment, many=True).data,
            'equipment_with_alerts': equipment_with_alerts
        }
        
        return Response(dashboard_data)
