from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Alert
from .serializers import (
    AlertSerializer, AlertCreateSerializer, AlertUpdateSerializer,
    AlertDetailSerializer, AlertStatsSerializer, AlertAcknowledgeSerializer,
    AlertResolveSerializer
)


class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des alertes."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'equipment', 'equipment__site', 'equipment__site__company']
    search_fields = ['title', 'message', 'equipment__name', 'equipment__site__name']
    ordering_fields = ['created_at', 'resolved_at', 'type', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtre les alertes selon les permissions de l'utilisateur."""
        user = self.request.user
        
        if user.is_staff:
            queryset = Alert.objects.all()
        elif user.company:
            queryset = Alert.objects.filter(equipment__site__company=user.company)
        else:
            queryset = Alert.objects.none()
        
        # Filtres supplémentaires via query params
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        type_filter = self.request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        
        # Filtrer par période
        days = self.request.query_params.get('days')
        if days:
            try:
                days_int = int(days)
                start_date = timezone.now() - timedelta(days=days_int)
                queryset = queryset.filter(created_at__gte=start_date)
            except ValueError:
                pass
        
        # Filtrer par site
        site_id = self.request.query_params.get('site')
        if site_id:
            try:
                queryset = queryset.filter(equipment__site_id=int(site_id))
            except ValueError:
                pass
        
        # Filtrer par équipement
        equipment_id = self.request.query_params.get('equipment')
        if equipment_id:
            try:
                queryset = queryset.filter(equipment_id=int(equipment_id))
            except ValueError:
                pass
        
        return queryset.select_related(
            'equipment', 
            'equipment__site', 
            'equipment__site__company'
        )
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action."""
        if self.action == 'create':
            return AlertCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AlertUpdateSerializer
        elif self.action == 'retrieve':
            return AlertDetailSerializer
        return AlertSerializer
    
    def perform_create(self, serializer):
        """Personnalise la création d'alerte."""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acquitte une alerte."""
        alert = self.get_object()
        if alert.status == 'active':
            alert.status = 'acknowledged'
            alert.save()
            return Response({'message': 'Alerte acquittée'})
        return Response(
            {'error': 'Seules les alertes actives peuvent être acquittées'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Résout une alerte."""
        alert = self.get_object()
        if alert.status in ['active', 'acknowledged']:
            alert.status = 'resolved'
            alert.resolved_at = timezone.now()
            alert.save()
            return Response({'message': 'Alerte résolue'})
        return Response(
            {'error': 'Seules les alertes ouvertes ou acquittées peuvent être résolues'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Rouvre une alerte résolue."""
        alert = self.get_object()
        if alert.status == 'resolved':
            alert.status = 'active'
            alert.resolved_at = None
            alert.save()
            return Response({'message': 'Alerte rouverte'})
        return Response(
            {'error': 'Seules les alertes résolues peuvent être rouvertes'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des alertes."""
        queryset = self.get_queryset()
        
        # Statistiques générales
        total_alerts = queryset.count()
        active_alerts = queryset.filter(status='active').count()
        acknowledged_alerts = queryset.filter(status='acknowledged').count()
        resolved_alerts = queryset.filter(status='resolved').count()
        
        # Alertes par type
        alerts_by_type = dict(
            queryset.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )
        
        # Alertes par site
        alerts_by_site = dict(
            queryset.values('equipment__site__name')
            .annotate(count=Count('id'))
            .values_list('equipment__site__name', 'count')
        )
        
        # Temps moyen de résolution (en secondes)
        resolved_queryset = queryset.filter(
            status='resolved',
            resolved_at__isnull=False
        )
        
        avg_resolution_time = 0
        if resolved_queryset.exists():
            # Calcul manuel du temps moyen de résolution
            total_time = 0
            count = 0
            for alert in resolved_queryset:
                if alert.resolved_at and alert.created_at:
                    duration = (alert.resolved_at - alert.created_at).total_seconds()
                    total_time += duration
                    count += 1
            
            if count > 0:
                avg_resolution_time = total_time / count
        
        stats_data = {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'acknowledged_alerts': acknowledged_alerts,
            'resolved_alerts': resolved_alerts,
            'alerts_by_type': alerts_by_type,
            'alerts_by_site': alerts_by_site,
            'average_resolution_time': avg_resolution_time
        }
        
        serializer = AlertStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Alertes critiques non résolues."""
        critical_alerts = self.get_queryset().filter(
            type='error',
            status__in=['active', 'acknowledged']
        ).order_by('-created_at')
        
        page = self.paginate_queryset(critical_alerts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(critical_alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Alertes récentes (dernières 24h)."""
        hours = int(request.query_params.get('hours', 24))
        start_time = timezone.now() - timedelta(hours=hours)
        
        recent_alerts = self.get_queryset().filter(
            created_at__gte=start_time
        ).order_by('-created_at')
        
        page = self.paginate_queryset(recent_alerts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(recent_alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Alertes actives uniquement."""
        active_alerts = self.get_queryset().filter(
            status='active'
        ).order_by('-created_at')
        
        page = self.paginate_queryset(active_alerts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_acknowledge(self, request):
        """Acquitte plusieurs alertes en masse."""
        serializer = AlertAcknowledgeSerializer(data=request.data)
        if serializer.is_valid():
            alert_ids = serializer.validated_data['alert_ids']
            
            alerts = self.get_queryset().filter(
                id__in=alert_ids,
                status='active'
            )
            
            updated_count = alerts.update(status='acknowledged')
            return Response({
                'message': f'{updated_count} alertes acquittées'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def bulk_resolve(self, request):
        """Résout plusieurs alertes en masse."""
        serializer = AlertResolveSerializer(data=request.data)
        if serializer.is_valid():
            alert_ids = serializer.validated_data['alert_ids']
            resolution_message = serializer.validated_data.get('resolution_message', '')
            
            alerts = self.get_queryset().filter(
                id__in=alert_ids,
                status__in=['active', 'acknowledged']
            )
            
            now = timezone.now()
            updated_count = alerts.update(
                status='resolved',
                resolved_at=now
            )
            
            return Response({
                'message': f'{updated_count} alertes résolues',
                'resolution_message': resolution_message
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Données pour le tableau de bord des alertes."""
        queryset = self.get_queryset()
        now = timezone.now()
        
        # Alertes par période
        last_24h = queryset.filter(created_at__gte=now - timedelta(hours=24)).count()
        last_7d = queryset.filter(created_at__gte=now - timedelta(days=7)).count()
        last_30d = queryset.filter(created_at__gte=now - timedelta(days=30)).count()
        
        # Alertes critiques actives
        critical_active = queryset.filter(
            type='error',
            status='active'
        ).count()
        
        # Top 5 des équipements avec le plus d'alertes
        top_equipment = list(
            queryset.values('equipment__name', 'equipment__id')
            .annotate(alert_count=Count('id'))
            .order_by('-alert_count')[:5]
        )
        
        # Top 5 des sites avec le plus d'alertes
        top_sites = list(
            queryset.values('equipment__site__name', 'equipment__site__id')
            .annotate(alert_count=Count('id'))
            .order_by('-alert_count')[:5]
        )
        
        dashboard_data = {
            'summary': {
                'total': queryset.count(),
                'active': queryset.filter(status='active').count(),
                'acknowledged': queryset.filter(status='acknowledged').count(),
                'resolved': queryset.filter(status='resolved').count(),
                'critical_active': critical_active
            },
            'timeline': {
                'last_24h': last_24h,
                'last_7d': last_7d,
                'last_30d': last_30d
            },
            'top_equipment': top_equipment,
            'top_sites': top_sites,
            'recent_alerts': AlertSerializer(
                queryset.order_by('-created_at')[:10], 
                many=True
            ).data
        }
        
        return Response(dashboard_data)
