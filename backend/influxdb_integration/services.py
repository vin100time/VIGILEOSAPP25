"""
Services pour l'intégration des équipements avec InfluxDB.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from equipment.models import Equipment
from .client import influxdb_manager
import logging
import random

logger = logging.getLogger(__name__)


class EquipmentMetricsService:
    """Service pour gérer les métriques des équipements."""
    
    @staticmethod
    def record_equipment_metric(equipment: Equipment, metric_name: str, value: float, 
                              additional_fields: Optional[Dict] = None):
        """
        Enregistre une métrique pour un équipement.
        
        Args:
            equipment: Instance de l'équipement
            metric_name: Nom de la métrique
            value: Valeur de la métrique
            additional_fields: Champs supplémentaires
        """
        tags = {
            'site_id': str(equipment.site_id),
            'site_name': equipment.site.name,
            'equipment_type': equipment.type,
            'equipment_name': equipment.name
        }
        
        if equipment.ip_address:
            tags['ip_address'] = equipment.ip_address
        
        influxdb_manager.write_equipment_metric(
            equipment_id=equipment.id,
            metric_name=metric_name,
            value=value,
            tags=tags,
            fields=additional_fields
        )
    
    @staticmethod
    def record_availability_check(equipment: Equipment, is_available: bool, 
                                response_time: Optional[float] = None):
        """
        Enregistre un contrôle de disponibilité.
        
        Args:
            equipment: Instance de l'équipement
            is_available: Si l'équipement est disponible
            response_time: Temps de réponse en ms
        """
        value = 1.0 if is_available else 0.0
        fields = {}
        
        if response_time is not None:
            fields['response_time_ms'] = response_time
        
        EquipmentMetricsService.record_equipment_metric(
            equipment=equipment,
            metric_name='availability',
            value=value,
            additional_fields=fields
        )
    
    @staticmethod
    def record_performance_metrics(equipment: Equipment, metrics: Dict[str, float]):
        """
        Enregistre plusieurs métriques de performance.
        
        Args:
            equipment: Instance de l'équipement
            metrics: Dictionnaire des métriques {nom: valeur}
        """
        for metric_name, value in metrics.items():
            EquipmentMetricsService.record_equipment_metric(
                equipment=equipment,
                metric_name=metric_name,
                value=value
            )
    
    @staticmethod
    def simulate_equipment_metrics(equipment: Equipment):
        """
        Simule des métriques pour un équipement (pour les tests).
        
        Args:
            equipment: Instance de l'équipement
        """
        # Disponibilité
        is_online = equipment.status == 'online'
        availability = 1.0 if is_online else 0.0
        response_time = random.uniform(10, 100) if is_online else None
        
        EquipmentMetricsService.record_availability_check(
            equipment=equipment,
            is_available=is_online,
            response_time=response_time
        )
        
        # Métriques spécifiques par type d'équipement
        if equipment.type == 'camera':
            metrics = {
                'fps': random.uniform(20, 30) if is_online else 0,
                'bitrate_mbps': random.uniform(2, 8) if is_online else 0,
                'packet_loss': random.uniform(0, 0.5) if is_online else 100
            }
        elif equipment.type == 'server':
            metrics = {
                'cpu_usage': random.uniform(10, 80) if is_online else 0,
                'memory_usage': random.uniform(30, 90) if is_online else 0,
                'disk_usage': random.uniform(20, 85) if is_online else 0,
                'temperature': random.uniform(40, 70) if is_online else 0
            }
        elif equipment.type == 'switch':
            metrics = {
                'bandwidth_usage': random.uniform(100, 1000) if is_online else 0,
                'port_errors': random.randint(0, 5) if is_online else 0,
                'uptime_hours': random.randint(100, 8760) if is_online else 0
            }
        else:
            metrics = {
                'health_score': random.uniform(70, 100) if is_online else 0
            }
        
        EquipmentMetricsService.record_performance_metrics(equipment, metrics)


class EquipmentAnalyticsService:
    """Service pour l'analyse des données d'équipement."""
    
    @staticmethod
    def get_equipment_dashboard_data(equipment_id: int, period: str = "24h") -> Dict:
        """
        Récupère les données pour le tableau de bord d'un équipement.
        
        Args:
            equipment_id: ID de l'équipement
            period: Période d'analyse (24h, 7d, 30d)
        
        Returns:
            Données du tableau de bord
        """
        start = f"-{period}"
        
        # Statistiques générales
        stats = influxdb_manager.get_equipment_statistics(equipment_id, start)
        
        # Métriques de disponibilité
        availability_data = influxdb_manager.query_equipment_metrics(
            equipment_id=equipment_id,
            metric_name='availability',
            start=start,
            aggregation='mean'
        )
        
        # Temps de réponse moyen
        response_time_data = influxdb_manager.query_equipment_metrics(
            equipment_id=equipment_id,
            metric_name='response_time_ms',
            start=start,
            aggregation='mean'
        )
        
        return {
            'statistics': stats,
            'availability_trend': availability_data,
            'response_time_trend': response_time_data,
            'period': period
        }
    
    @staticmethod
    def get_site_equipment_summary(site_id: int, period: str = "24h") -> Dict:
        """
        Récupère un résumé des équipements d'un site.
        
        Args:
            site_id: ID du site
            period: Période d'analyse
        
        Returns:
            Résumé des équipements du site
        """
        from equipment.models import Equipment
        
        equipments = Equipment.objects.filter(site_id=site_id)
        summary = {
            'total_equipment': equipments.count(),
            'online': 0,
            'offline': 0,
            'warning': 0,
            'average_availability': 0,
            'equipment_details': []
        }
        
        total_availability = 0
        
        for equipment in equipments:
            availability = influxdb_manager.calculate_equipment_availability(
                equipment_id=equipment.id,
                start=f"-{period}"
            )
            
            total_availability += availability
            
            # Compter par statut
            if equipment.status == 'online':
                summary['online'] += 1
            elif equipment.status == 'offline':
                summary['offline'] += 1
            else:
                summary['warning'] += 1
            
            summary['equipment_details'].append({
                'id': equipment.id,
                'name': equipment.name,
                'type': equipment.type,
                'status': equipment.status,
                'availability': availability
            })
        
        if equipments.count() > 0:
            summary['average_availability'] = round(total_availability / equipments.count(), 2)
        
        return summary
    
    @staticmethod
    def generate_availability_report(equipment_id: int, start_date: datetime, 
                                   end_date: datetime) -> Dict:
        """
        Génère un rapport de disponibilité détaillé.
        
        Args:
            equipment_id: ID de l'équipement
            start_date: Date de début
            end_date: Date de fin
        
        Returns:
            Rapport de disponibilité
        """
        start = start_date.isoformat() + "Z"
        stop = end_date.isoformat() + "Z"
        
        # Disponibilité globale
        overall_availability = influxdb_manager.calculate_equipment_availability(
            equipment_id=equipment_id,
            start=start,
            stop=stop
        )
        
        # Données horaires
        hourly_data = influxdb_manager.query_equipment_metrics(
            equipment_id=equipment_id,
            metric_name='availability',
            start=start,
            stop=stop,
            aggregation='mean'
        )
        
        # Calcul des périodes d'indisponibilité
        downtime_periods = []
        current_downtime = None
        
        for point in hourly_data:
            if point['value'] < 0.5:  # Considéré comme indisponible
                if not current_downtime:
                    current_downtime = {
                        'start': point['time'],
                        'end': point['time'],
                        'duration_hours': 1
                    }
                else:
                    current_downtime['end'] = point['time']
                    current_downtime['duration_hours'] += 1
            else:
                if current_downtime:
                    downtime_periods.append(current_downtime)
                    current_downtime = None
        
        if current_downtime:
            downtime_periods.append(current_downtime)
        
        total_hours = (end_date - start_date).total_seconds() / 3600
        total_downtime_hours = sum(p['duration_hours'] for p in downtime_periods)
        
        return {
            'equipment_id': equipment_id,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'total_hours': total_hours
            },
            'availability': {
                'percentage': overall_availability,
                'uptime_hours': total_hours - total_downtime_hours,
                'downtime_hours': total_downtime_hours
            },
            'downtime_periods': downtime_periods,
            'hourly_data': hourly_data
        }


# Signaux Django pour enregistrer automatiquement les changements de statut
@receiver(pre_save, sender=Equipment)
def track_status_change(sender, instance, **kwargs):
    """Enregistre les changements de statut avant la sauvegarde."""
    if instance.pk:
        try:
            old_instance = Equipment.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                # Stocker l'ancien statut pour l'utiliser dans post_save
                instance._old_status = old_instance.status
        except Equipment.DoesNotExist:
            pass


@receiver(post_save, sender=Equipment)
def record_status_change(sender, instance, created, **kwargs):
    """Enregistre le changement de statut dans InfluxDB."""
    if hasattr(instance, '_old_status'):
        tags = {
            'site_id': str(instance.site_id),
            'site_name': instance.site.name,
            'equipment_type': instance.type,
            'equipment_name': instance.name
        }
        
        influxdb_manager.write_equipment_status_change(
            equipment_id=instance.id,
            old_status=instance._old_status,
            new_status=instance.status,
            tags=tags
        )
        
        # Nettoyer l'attribut temporaire
        delattr(instance, '_old_status')
    
    elif created:
        # Nouvel équipement, enregistrer le statut initial
        tags = {
            'site_id': str(instance.site_id),
            'site_name': instance.site.name,
            'equipment_type': instance.type,
            'equipment_name': instance.name
        }
        
        influxdb_manager.write_equipment_status_change(
            equipment_id=instance.id,
            old_status='new',
            new_status=instance.status,
            tags=tags
        )