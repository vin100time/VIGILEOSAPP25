from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'status', 'site']
    search_fields = ['name', 'ip_address']
    ordering_fields = ['name', 'created_at', 'last_maintenance']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Filtrer les équipements par l'entreprise de l'utilisateur
        queryset = Equipment.objects.filter(site__company=self.request.user.company)
        
        # Recherche textuelle
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(ip_address__icontains=search) |
                Q(site__name__icontains=search)
            )
        
        return queryset.select_related('site')
    
    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        """Récupérer les alertes d'un équipement"""
        equipment = self.get_object()
        alerts = equipment.alerts.all().order_by('-created_at')[:10]
        from alerts.serializers import AlertSerializer
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        """Récupérer les métriques récentes d'un équipement"""
        equipment = self.get_object()
        # Limiter aux 100 dernières métriques
        metrics = equipment.metrics.all()[:100]
        from metrics.serializers import NetworkMetricSerializer
        serializer = NetworkMetricSerializer(metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def maintenance(self, request, pk=None):
        """Marquer un équipement en maintenance"""
        equipment = self.get_object()
        equipment.status = 'maintenance'
        equipment.save()
        return Response({'status': 'Équipement mis en maintenance'})
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un équipement"""
        equipment = self.get_object()
        equipment.status = 'active'
        equipment.save()
        return Response({'status': 'Équipement activé'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des équipements"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(status='active').count(),
            'inactive': queryset.filter(status='inactive').count(),
            'maintenance': queryset.filter(status='maintenance').count(),
            'by_type': {}
        }
        
        # Statistiques par type
        for equipment_type in Equipment.TYPE_CHOICES:
            type_code = equipment_type[0]
            stats['by_type'][type_code] = queryset.filter(type=type_code).count()
        
        return Response(stats)
