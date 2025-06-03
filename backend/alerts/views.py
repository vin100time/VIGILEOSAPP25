from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from .models import Alert
from .serializers import AlertSerializer

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'equipment', 'equipment__site']
    search_fields = ['title', 'message', 'equipment__name']
    ordering_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Filtrer les alertes par l'entreprise de l'utilisateur
        queryset = Alert.objects.filter(equipment__site__company=self.request.user.company)
        
        # Filtres supplémentaires
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtrer par période
        days = self.request.query_params.get('days', None)
        if days:
            try:
                days_int = int(days)
                start_date = timezone.now() - timezone.timedelta(days=days_int)
                queryset = queryset.filter(created_at__gte=start_date)
            except ValueError:
                pass
        
        return queryset.select_related('equipment', 'equipment__site')
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acquitter une alerte"""
        alert = self.get_object()
        if alert.status == 'active':
            alert.status = 'acknowledged'
            alert.save()
            return Response({'status': 'Alerte acquittée'})
        return Response(
            {'error': 'Seules les alertes actives peuvent être acquittées'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Résoudre une alerte"""
        alert = self.get_object()
        if alert.status in ['active', 'acknowledged']:
            alert.status = 'resolved'
            alert.resolved_at = timezone.now()
            alert.save()
            return Response({'status': 'Alerte résolue'})
        return Response(
            {'error': 'Seules les alertes ouvertes ou acquittées peuvent être résolues'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des alertes"""
        queryset = self.get_queryset()
        
        # Statistiques générales
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(status='active').count(),
            'acknowledged': queryset.filter(status='acknowledged').count(),
            'resolved': queryset.filter(status='resolved').count(),
            'by_type': {},
            'recent': queryset.filter(
                created_at__gte=timezone.now() - timezone.timedelta(hours=24)
            ).count()
        }
        
        # Statistiques par type
        for alert_type in Alert.TYPE_CHOICES:
            type_code = alert_type[0]
            stats['by_type'][type_code] = queryset.filter(type=type_code).count()
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Alertes critiques non résolues"""
        critical_alerts = self.get_queryset().filter(
            type='error',
            status__in=['active', 'acknowledged']
        ).order_by('-created_at')
        
        serializer = self.get_serializer(critical_alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_acknowledge(self, request):
        """Acquitter plusieurs alertes en masse"""
        alert_ids = request.data.get('alert_ids', [])
        if not alert_ids:
            return Response(
                {'error': 'Aucun ID d\'alerte fourni'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alerts = self.get_queryset().filter(
            id__in=alert_ids,
            status='active'
        )
        
        updated_count = alerts.update(status='acknowledged')
        return Response({
            'status': f'{updated_count} alertes acquittées'
        })
