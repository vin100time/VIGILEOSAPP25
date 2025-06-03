from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import NetworkMetric, AlertThreshold
from .serializers import (
    NetworkMetricSerializer, NetworkMetricCreateSerializer,
    AlertThresholdSerializer, MetricsSummarySerializer
)

class NetworkMetricViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['equipment', 'is_online', 'connection_quality']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        # Filtrer les métriques par l'entreprise de l'utilisateur
        return NetworkMetric.objects.filter(
            equipment__site__company=self.request.user.company
        ).select_related('equipment', 'equipment__site')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NetworkMetricCreateSerializer
        return NetworkMetricSerializer
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Résumé des métriques par équipement"""
        queryset = self.get_queryset()
        
        # Filtrer par période (défaut: 24h)
        hours = int(request.query_params.get('hours', 24))
        start_time = timezone.now() - timedelta(hours=hours)
        queryset = queryset.filter(timestamp__gte=start_time)
        
        # Agrégation par équipement
        summary_data = []
        equipment_ids = queryset.values_list('equipment_id', flat=True).distinct()
        
        for equipment_id in equipment_ids:
            equipment_metrics = queryset.filter(equipment_id=equipment_id)
            equipment = equipment_metrics.first().equipment
            
            # Calculs d'agrégation
            aggregates = equipment_metrics.aggregate(
                avg_ping=Avg('ping_response_time'),
                avg_cpu=Avg('cpu_usage'),
                total_measurements=Count('id')
            )
            
            # Calcul du pourcentage d'uptime
            online_count = equipment_metrics.filter(is_online=True).count()
            uptime_percentage = (online_count / aggregates['total_measurements'] * 100) if aggregates['total_measurements'] > 0 else 0
            
            # Calcul des moyennes d'utilisation mémoire et disque
            memory_usage_avg = 0
            disk_usage_avg = 0
            
            for metric in equipment_metrics:
                if metric.memory_usage_percent:
                    memory_usage_avg += metric.memory_usage_percent
                if metric.disk_usage_percent:
                    disk_usage_avg += metric.disk_usage_percent
            
            count = aggregates['total_measurements']
            if count > 0:
                memory_usage_avg /= count
                disk_usage_avg /= count
            
            summary_data.append({
                'equipment_id': equipment_id,
                'equipment_name': equipment.name,
                'site_name': equipment.site.name,
                'latest_timestamp': equipment_metrics.first().timestamp,
                'avg_ping': aggregates['avg_ping'],
                'avg_cpu': aggregates['avg_cpu'],
                'avg_memory_usage': memory_usage_avg,
                'avg_disk_usage': disk_usage_avg,
                'uptime_percentage': uptime_percentage,
                'total_measurements': count
            })
        
        serializer = MetricsSummarySerializer(summary_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Dernières métriques pour tous les équipements"""
        # Récupérer la dernière métrique pour chaque équipement
        latest_metrics = []
        equipment_ids = self.get_queryset().values_list('equipment_id', flat=True).distinct()
        
        for equipment_id in equipment_ids:
            latest_metric = self.get_queryset().filter(equipment_id=equipment_id).first()
            if latest_metric:
                latest_metrics.append(latest_metric)
        
        serializer = self.get_serializer(latest_metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Création en masse de métriques"""
        serializer = NetworkMetricCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': f'{len(serializer.data)} métriques créées'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlertThresholdViewSet(viewsets.ModelViewSet):
    serializer_class = AlertThresholdSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['equipment']
    
    def get_queryset(self):
        # Filtrer les seuils par l'entreprise de l'utilisateur
        return AlertThreshold.objects.filter(
            equipment__site__company=self.request.user.company
        ).select_related('equipment', 'equipment__site')
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Mise à jour en masse des seuils"""
        equipment_ids = request.data.get('equipment_ids', [])
        threshold_data = request.data.get('thresholds', {})
        
        if not equipment_ids or not threshold_data:
            return Response(
                {'error': 'equipment_ids et thresholds sont requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = 0
        for equipment_id in equipment_ids:
            threshold, created = AlertThreshold.objects.get_or_create(
                equipment_id=equipment_id,
                defaults=threshold_data
            )
            if not created:
                for key, value in threshold_data.items():
                    setattr(threshold, key, value)
                threshold.save()
            updated_count += 1
        
        return Response({
            'status': f'{updated_count} seuils mis à jour'
        })
