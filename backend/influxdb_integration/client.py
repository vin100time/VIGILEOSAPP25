"""
Client InfluxDB pour la gestion de la connexion et des opérations de base.
"""
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class InfluxDBManager:
    """Gestionnaire pour les opérations InfluxDB."""
    
    def __init__(self):
        """Initialise la connexion à InfluxDB."""
        self.url = getattr(settings, 'INFLUXDB_URL', os.environ.get('INFLUXDB_URL', 'http://influxdb:8086'))
        self.token = getattr(settings, 'INFLUXDB_TOKEN', os.environ.get('INFLUXDB_TOKEN', ''))
        self.org = getattr(settings, 'INFLUXDB_ORG', os.environ.get('INFLUXDB_ORG', 'vigileos'))
        self.bucket = getattr(settings, 'INFLUXDB_BUCKET', os.environ.get('INFLUXDB_BUCKET', 'equipment_metrics'))
        
        self.client = None
        self.write_api = None
        self.query_api = None
        
        if self.token:
            self._connect()
    
    def _connect(self):
        """Établit la connexion avec InfluxDB."""
        try:
            self.client = InfluxDBClient(
                url=self.url,
                token=self.token,
                org=self.org
            )
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            logger.info(f"Connexion établie avec InfluxDB à {self.url}")
        except Exception as e:
            logger.error(f"Erreur de connexion à InfluxDB: {e}")
            raise
    
    def write_equipment_metric(self, equipment_id: int, metric_name: str, value: float, 
                             tags: Optional[Dict[str, str]] = None, 
                             fields: Optional[Dict[str, Any]] = None,
                             timestamp: Optional[datetime] = None):
        """
        Écrit une métrique d'équipement dans InfluxDB.
        
        Args:
            equipment_id: ID de l'équipement
            metric_name: Nom de la métrique (ex: 'availability', 'cpu_usage', 'temperature')
            value: Valeur de la métrique
            tags: Tags supplémentaires (ex: {'site': 'Paris', 'type': 'camera'})
            fields: Champs supplémentaires
            timestamp: Timestamp de la métrique (par défaut: maintenant)
        """
        if not self.write_api:
            logger.warning("InfluxDB non configuré, métrique non enregistrée")
            return
        
        try:
            point = Point("equipment_metrics") \
                .tag("equipment_id", str(equipment_id)) \
                .tag("metric_name", metric_name)
            
            if tags:
                for key, val in tags.items():
                    point = point.tag(key, str(val))
            
            point = point.field("value", float(value))
            
            if fields:
                for key, val in fields.items():
                    point = point.field(key, val)
            
            if timestamp:
                point = point.time(timestamp, WritePrecision.NS)
            
            self.write_api.write(bucket=self.bucket, record=point)
            logger.debug(f"Métrique écrite: {metric_name}={value} pour equipment_id={equipment_id}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture de la métrique: {e}")
            raise
    
    def write_equipment_status_change(self, equipment_id: int, old_status: str, 
                                    new_status: str, tags: Optional[Dict[str, str]] = None):
        """
        Enregistre un changement de statut d'équipement.
        
        Args:
            equipment_id: ID de l'équipement
            old_status: Ancien statut
            new_status: Nouveau statut
            tags: Tags supplémentaires
        """
        try:
            point = Point("equipment_status_changes") \
                .tag("equipment_id", str(equipment_id)) \
                .tag("old_status", old_status) \
                .tag("new_status", new_status)
            
            if tags:
                for key, val in tags.items():
                    point = point.tag(key, str(val))
            
            # Valeur numérique pour faciliter les calculs
            status_values = {'online': 1, 'offline': 0, 'warning': 0.5}
            point = point.field("status_value", status_values.get(new_status, -1))
            point = point.field("change_event", 1)
            
            self.write_api.write(bucket=self.bucket, record=point)
            logger.info(f"Changement de statut enregistré: {equipment_id} {old_status} -> {new_status}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du changement de statut: {e}")
            raise
    
    def query_equipment_metrics(self, equipment_id: int, metric_name: str, 
                              start: str = "-24h", stop: str = "now",
                              aggregation: Optional[str] = None) -> List[Dict]:
        """
        Récupère les métriques d'un équipement.
        
        Args:
            equipment_id: ID de l'équipement
            metric_name: Nom de la métrique
            start: Début de la période (ex: "-24h", "-7d", "2024-01-01T00:00:00Z")
            stop: Fin de la période (ex: "now", "2024-01-02T00:00:00Z")
            aggregation: Type d'agrégation (mean, max, min, sum, count)
        
        Returns:
            Liste des points de données
        """
        if not self.query_api:
            logger.warning("InfluxDB non configuré")
            return []
        
        try:
            if aggregation:
                query = f'''
                from(bucket: "{self.bucket}")
                    |> range(start: {start}, stop: {stop})
                    |> filter(fn: (r) => r["_measurement"] == "equipment_metrics")
                    |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
                    |> filter(fn: (r) => r["metric_name"] == "{metric_name}")
                    |> filter(fn: (r) => r["_field"] == "value")
                    |> aggregateWindow(every: 1h, fn: {aggregation}, createEmpty: false)
                '''
            else:
                query = f'''
                from(bucket: "{self.bucket}")
                    |> range(start: {start}, stop: {stop})
                    |> filter(fn: (r) => r["_measurement"] == "equipment_metrics")
                    |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
                    |> filter(fn: (r) => r["metric_name"] == "{metric_name}")
                    |> filter(fn: (r) => r["_field"] == "value")
                '''
            
            result = self.query_api.query(query=query)
            
            data = []
            for table in result:
                for record in table.records:
                    data.append({
                        'time': record.get_time(),
                        'value': record.get_value(),
                        'equipment_id': record.values.get('equipment_id'),
                        'metric_name': record.values.get('metric_name')
                    })
            
            return data
            
        except Exception as e:
            logger.error(f"Erreur lors de la requête: {e}")
            raise
    
    def calculate_equipment_availability(self, equipment_id: int, start: str = "-24h", 
                                       stop: str = "now") -> float:
        """
        Calcule le taux de disponibilité d'un équipement sur une période.
        
        Args:
            equipment_id: ID de l'équipement
            start: Début de la période
            stop: Fin de la période
        
        Returns:
            Taux de disponibilité en pourcentage (0-100)
        """
        if not self.query_api:
            return 0.0
        
        try:
            query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: {start}, stop: {stop})
                |> filter(fn: (r) => r["_measurement"] == "equipment_status_changes")
                |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
                |> filter(fn: (r) => r["_field"] == "status_value")
                |> mean()
            '''
            
            result = self.query_api.query(query=query)
            
            if result and result[0].records:
                # La valeur moyenne donne le taux de disponibilité
                availability = result[0].records[0].get_value() * 100
                return round(availability, 2)
            
            return 100.0  # Si pas de données, on considère l'équipement comme disponible
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de disponibilité: {e}")
            return 0.0
    
    def get_equipment_statistics(self, equipment_id: int, start: str = "-7d") -> Dict:
        """
        Récupère des statistiques complètes pour un équipement.
        
        Args:
            equipment_id: ID de l'équipement
            start: Début de la période d'analyse
        
        Returns:
            Dictionnaire avec les statistiques
        """
        stats = {
            'availability': self.calculate_equipment_availability(equipment_id, start),
            'status_changes': 0,
            'current_status': 'unknown',
            'metrics': {}
        }
        
        try:
            # Compter les changements de statut
            query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: {start})
                |> filter(fn: (r) => r["_measurement"] == "equipment_status_changes")
                |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
                |> filter(fn: (r) => r["_field"] == "change_event")
                |> count()
            '''
            
            result = self.query_api.query(query=query)
            if result and result[0].records:
                stats['status_changes'] = result[0].records[0].get_value()
            
            # Récupérer le dernier statut
            query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: {start})
                |> filter(fn: (r) => r["_measurement"] == "equipment_status_changes")
                |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
                |> last()
            '''
            
            result = self.query_api.query(query=query)
            for table in result:
                for record in table.records:
                    if 'new_status' in record.values:
                        stats['current_status'] = record.values['new_status']
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return stats
    
    def close(self):
        """Ferme la connexion à InfluxDB."""
        if self.client:
            self.client.close()
            logger.info("Connexion InfluxDB fermée")


# Instance singleton
influxdb_manager = InfluxDBManager()