from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Site
from .serializers import (
    SiteSerializer, SiteCreateSerializer, SiteUpdateSerializer,
    SiteDetailSerializer, SiteStatsSerializer, SiteBulkUpdateSerializer
)


class SiteViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des sites."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at', 'updated_at', 'status']
    ordering = ['name']
    
    def get_queryset(self):
        """Filtre les sites selon les permissions de l'utilisateur."""
        user = self.request.user
        
        if user.is_staff:
            queryset = Site.objects.all()
        elif user.company:
            queryset = Site.objects.filter(company=user.company)
        else:
            queryset = Site.objects.none()
        
        return queryset.select_related('company')
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action."""
        if self.action == 'create':
            return SiteCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SiteUpdateSerializer
        elif self.action == 'retrieve':
            return SiteDetailSerializer
        return SiteSerializer
    
    def perform_create(self, serializer):
        """Personnalise la création de site."""
        # Si l'utilisateur n'est pas staff, assigne automatiquement son entreprise
        if not self.request.user.is_staff and self.request.user.company:
            serializer.save(company=self.request.user.company)
        else:
            serializer.save()
    
    @action(detail=True, methods=['get'])
    def equipment(self, request, pk=None):
        """Récupère tous les équipements d'un site."""
        site = self.get_object()
        equipment = site.equipment.all()
        
        # Filtrer par type si spécifié
        equipment_type = request.query_params.get('type')
        if equipment_type:
            equipment = equipment.filter(type=equipment_type)
        
        # Filtrer par statut si spécifié
        equipment_status = request.query_params.get('status')
        if equipment_status:
            equipment = equipment.filter(status=equipment_status)
        
        # Pagination
        page = self.paginate_queryset(equipment)
        if page is not None:
            from equipment.serializers import EquipmentSerializer
            serializer = EquipmentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        from equipment.serializers import EquipmentSerializer
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        """Récupère toutes les alertes d'un site."""
        site = self.get_object()
        
        # Récupérer les alertes via les équipements du site
        from alerts.models import Alert
        alerts = Alert.objects.filter(equipment__site=site)
        
        # Filtrer par statut si spécifié
        alert_status = request.query_params.get('status')
        if alert_status:
            alerts = alerts.filter(status=alert_status)
        
        # Filtrer par type si spécifié
        alert_type = request.query_params.get('type')
        if alert_type:
            alerts = alerts.filter(type=alert_type)
        
        # Ordonner par date de création
        alerts = alerts.order_by('-created_at')
        
        # Pagination
        page = self.paginate_queryset(alerts)
        if page is not None:
            from alerts.serializers import AlertSerializer
            serializer = AlertSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        from alerts.serializers import AlertSerializer
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def site_stats(self, request, pk=None):
        """Statistiques détaillées d'un site."""
        site = self.get_object()
        
        # Statistiques des équipements
        total_equipment = site.equipment.count()
        equipment_by_status = dict(
            site.equipment.values('status')
            .annotate(count=Count('id'))
            .values_list('status', 'count')
        )
        equipment_by_type = dict(
            site.equipment.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )
        
        # Statistiques des alertes
        from alerts.models import Alert
        site_alerts = Alert.objects.filter(equipment__site=site)
        total_alerts = site_alerts.count()
        active_alerts = site_alerts.filter(status='active').count()
        alerts_by_type = dict(
            site_alerts.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )
        
        # Maintenance
        from django.utils import timezone
        from datetime import timedelta
        one_year_ago = timezone.now().date() - timedelta(days=365)
        maintenance_overdue = site.equipment.filter(
            Q(last_maintenance__lt=one_year_ago) | Q(last_maintenance__isnull=True)
        ).count()
        
        stats_data = {
            'equipment': {
                'total': total_equipment,
                'by_status': equipment_by_status,
                'by_type': equipment_by_type,
                'maintenance_overdue': maintenance_overdue
            },
            'alerts': {
                'total': total_alerts,
                'active': active_alerts,
                'by_type': alerts_by_type
            }
        }
        
        return Response(stats_data)
    
    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        """Change le statut d'un site."""
        site = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in [choice[0] for choice in Site.STATUS_CHOICES]:
            return Response(
                {'error': 'Statut invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = site.status
        site.status = new_status
        site.save()
        
        return Response({
            'message': f'Statut du site changé de {old_status} à {new_status}',
            'old_status': old_status,
            'new_status': new_status
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques générales des sites."""
        queryset = self.get_queryset()
        
        # Statistiques générales
        total_sites = queryset.count()
        online_sites = queryset.filter(status='online').count()
        offline_sites = queryset.filter(status='offline').count()
        warning_sites = queryset.filter(status='warning').count()
        pending_sites = queryset.filter(status='pending').count()
        
        # Sites par entreprise
        sites_by_company = dict(
            queryset.values('company__name')
            .annotate(count=Count('id'))
            .values_list('company__name', 'count')
        )
        
        # Moyenne d'équipements par site
        total_equipment = sum(site.equipment.count() for site in queryset)
        average_equipment_per_site = total_equipment / total_sites if total_sites > 0 else 0
        
        stats_data = {
            'total_sites': total_sites,
            'online_sites': online_sites,
            'offline_sites': offline_sites,
            'warning_sites': warning_sites,
            'pending_sites': pending_sites,
            'sites_by_company': sites_by_company,
            'average_equipment_per_site': average_equipment_per_site
        }
        
        serializer = SiteStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Sites groupés par statut."""
        queryset = self.get_queryset()
        status_filter = request.query_params.get('status')
        
        if status_filter:
            sites = queryset.filter(status=status_filter)
            page = self.paginate_queryset(sites)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(sites, many=True)
            return Response(serializer.data)
        
        # Retourner tous les statuts
        result = {}
        for status_choice in Site.STATUS_CHOICES:
            status_code = status_choice[0]
            sites = queryset.filter(status=status_code)
            result[status_code] = {
                'count': sites.count(),
                'sites': SiteSerializer(sites[:10], many=True).data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Sites en attente de validation."""
        pending_sites = self.get_queryset().filter(status='pending')
        
        page = self.paginate_queryset(pending_sites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(pending_sites, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def with_alerts(self, request):
        """Sites ayant des alertes actives."""
        from alerts.models import Alert
        
        # Sites avec des alertes actives
        sites_with_alerts = self.get_queryset().filter(
            equipment__alerts__status='active'
        ).distinct().annotate(
            active_alerts_count=Count('equipment__alerts', filter=Q(equipment__alerts__status='active'))
        ).order_by('-active_alerts_count')
        
        page = self.paginate_queryset(sites_with_alerts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(sites_with_alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Met à jour plusieurs sites en masse."""
        serializer = SiteBulkUpdateSerializer(data=request.data)
        if serializer.is_valid():
            site_ids = serializer.validated_data['site_ids']
            update_data = {}
            
            if 'status' in serializer.validated_data:
                update_data['status'] = serializer.validated_data['status']
            
            if update_data:
                sites = self.get_queryset().filter(id__in=site_ids)
                updated_count = sites.update(**update_data)
                
                return Response({
                    'message': f'{updated_count} sites mis à jour',
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
        """Données pour le tableau de bord des sites."""
        queryset = self.get_queryset()
        
        # Statistiques générales
        total = queryset.count()
        online = queryset.filter(status='online').count()
        offline = queryset.filter(status='offline').count()
        warning = queryset.filter(status='warning').count()
        pending = queryset.filter(status='pending').count()
        
        # Sites récemment ajoutés
        recent_sites = queryset.order_by('-created_at')[:5]
        
        # Sites avec le plus d'équipements
        sites_with_most_equipment = []
        for site in queryset.annotate(
            equipment_count=Count('equipment')
        ).filter(equipment_count__gt=0).order_by('-equipment_count')[:5]:
            sites_with_most_equipment.append({
                'id': site.id,
                'name': site.name,
                'equipment_count': site.equipment_count
            })
        
        # Sites avec le plus d'alertes actives
        sites_with_most_alerts = []
        for site in queryset.annotate(
            active_alerts=Count('equipment__alerts', filter=Q(equipment__alerts__status='active'))
        ).filter(active_alerts__gt=0).order_by('-active_alerts')[:5]:
            sites_with_most_alerts.append({
                'id': site.id,
                'name': site.name,
                'active_alerts': site.active_alerts
            })
        
        dashboard_data = {
            'summary': {
                'total': total,
                'online': online,
                'offline': offline,
                'warning': warning,
                'pending': pending
            },
            'recent_sites': SiteSerializer(recent_sites, many=True).data,
            'sites_with_most_equipment': sites_with_most_equipment,
            'sites_with_most_alerts': sites_with_most_alerts
        }
        
        return Response(dashboard_data)
