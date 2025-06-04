"""
Vues API pour les métriques InfluxDB.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from equipment.models import Equipment
from .services import EquipmentMetricsService, EquipmentAnalyticsService
from .client import influxdb_manager


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_equipment_metric(request, equipment_id):
    """
    Enregistre une métrique pour un équipement.
    
    POST /api/equipment/{equipment_id}/metrics/
    {
        "metric_name": "cpu_usage",
        "value": 75.5,
        "additional_fields": {
            "process_count": 125
        }
    }
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    metric_name = request.data.get('metric_name')
    value = request.data.get('value')
    
    if not metric_name or value is None:
        return Response(
            {'error': 'metric_name et value sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        value = float(value)
    except (TypeError, ValueError):
        return Response(
            {'error': 'value doit être un nombre'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    additional_fields = request.data.get('additional_fields', {})
    
    try:
        EquipmentMetricsService.record_equipment_metric(
            equipment=equipment,
            metric_name=metric_name,
            value=value,
            additional_fields=additional_fields
        )
        
        return Response({
            'message': 'Métrique enregistrée avec succès',
            'equipment_id': equipment_id,
            'metric_name': metric_name,
            'value': value
        })
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'enregistrement: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_availability_check(request, equipment_id):
    """
    Enregistre un contrôle de disponibilité.
    
    POST /api/equipment/{equipment_id}/availability/
    {
        "is_available": true,
        "response_time": 45.2
    }
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    is_available = request.data.get('is_available')
    if is_available is None:
        return Response(
            {'error': 'is_available est requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    response_time = request.data.get('response_time')
    if response_time is not None:
        try:
            response_time = float(response_time)
        except (TypeError, ValueError):
            response_time = None
    
    try:
        EquipmentMetricsService.record_availability_check(
            equipment=equipment,
            is_available=bool(is_available),
            response_time=response_time
        )
        
        # Mettre à jour le statut si nécessaire
        new_status = 'online' if is_available else 'offline'
        if equipment.status != new_status:
            equipment.status = new_status
            equipment.save()
        
        return Response({
            'message': 'Contrôle de disponibilité enregistré',
            'equipment_id': equipment_id,
            'is_available': is_available,
            'response_time': response_time
        })
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'enregistrement: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment_metrics(request, equipment_id):
    """
    Récupère les métriques d'un équipement.
    
    GET /api/equipment/{equipment_id}/metrics/?metric_name=cpu_usage&period=24h
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    metric_name = request.query_params.get('metric_name', 'availability')
    period = request.query_params.get('period', '24h')
    aggregation = request.query_params.get('aggregation')
    
    # Valider la période
    valid_periods = ['1h', '6h', '12h', '24h', '7d', '30d']
    if not any(period.endswith(p) for p in ['h', 'd', 'w', 'm']):
        period = '24h'
    
    try:
        data = influxdb_manager.query_equipment_metrics(
            equipment_id=equipment_id,
            metric_name=metric_name,
            start=f'-{period}',
            aggregation=aggregation
        )
        
        return Response({
            'equipment': {
                'id': equipment.id,
                'name': equipment.name,
                'type': equipment.type
            },
            'metric_name': metric_name,
            'period': period,
            'aggregation': aggregation,
            'data_points': len(data),
            'data': data
        })
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la récupération: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment_dashboard(request, equipment_id):
    """
    Récupère les données du tableau de bord d'un équipement.
    
    GET /api/equipment/{equipment_id}/dashboard/?period=24h
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    period = request.query_params.get('period', '24h')
    
    try:
        dashboard_data = EquipmentAnalyticsService.get_equipment_dashboard_data(
            equipment_id=equipment_id,
            period=period
        )
        
        dashboard_data['equipment'] = {
            'id': equipment.id,
            'name': equipment.name,
            'type': equipment.type,
            'status': equipment.status,
            'site': equipment.site.name,
            'ip_address': equipment.ip_address,
            'last_maintenance': equipment.last_maintenance
        }
        
        return Response(dashboard_data)
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la récupération: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_site_equipment_summary(request, site_id):
    """
    Récupère le résumé des équipements d'un site.
    
    GET /api/sites/{site_id}/equipment-summary/?period=24h
    """
    period = request.query_params.get('period', '24h')
    
    try:
        summary = EquipmentAnalyticsService.get_site_equipment_summary(
            site_id=site_id,
            period=period
        )
        
        return Response(summary)
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la récupération: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_availability_report(request, equipment_id):
    """
    Génère un rapport de disponibilité.
    
    GET /api/equipment/{equipment_id}/availability-report/?start=2024-01-01&end=2024-01-31
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    # Dates par défaut: derniers 30 jours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Parser les dates des paramètres
    start_param = request.query_params.get('start')
    end_param = request.query_params.get('end')
    
    if start_param:
        try:
            start_date = datetime.fromisoformat(start_param.replace('Z', '+00:00'))
        except ValueError:
            return Response(
                {'error': 'Format de date invalide pour start'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if end_param:
        try:
            end_date = datetime.fromisoformat(end_param.replace('Z', '+00:00'))
        except ValueError:
            return Response(
                {'error': 'Format de date invalide pour end'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    try:
        report = EquipmentAnalyticsService.generate_availability_report(
            equipment_id=equipment_id,
            start_date=start_date,
            end_date=end_date
        )
        
        report['equipment'] = {
            'id': equipment.id,
            'name': equipment.name,
            'type': equipment.type,
            'site': equipment.site.name
        }
        
        return Response(report)
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la génération du rapport: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )