from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json

from equipment.models import Equipment, Site
from .services import EquipmentMetricsService, EquipmentAnalyticsService
from .client import InfluxDBManager

User = get_user_model()


class InfluxDBManagerTestCase(TestCase):
    """Tests pour le client InfluxDB"""
    
    def setUp(self):
        self.manager = InfluxDBManager()
    
    @patch('influxdb_client.InfluxDBClient')
    def test_connection(self, mock_client):
        """Test de la connexion à InfluxDB"""
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.ping.return_value = True
        
        result = self.manager.test_connection()
        self.assertTrue(result)
    
    @patch('influxdb_client.InfluxDBClient')
    def test_write_data(self, mock_client):
        """Test de l'écriture de données"""
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        data = {
            'measurement': 'test_metric',
            'tags': {'equipment_id': '1'},
            'fields': {'value': 42.0},
            'time': datetime.now()
        }
        
        result = self.manager.write_data(data)
        self.assertTrue(result)
    
    @patch('influxdb_client.InfluxDBClient')
    def test_query_data(self, mock_client):
        """Test de la requête de données"""
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        query = 'from(bucket: "test") |> range(start: -1h)'
        mock_instance.query_api.return_value.query.return_value = []
        
        result = self.manager.query_data(query)
        self.assertIsInstance(result, list)


class EquipmentMetricsServiceTestCase(TestCase):
    """Tests pour le service de métriques"""
    
    def setUp(self):
        self.service = EquipmentMetricsService()
        
        # Créer des données de test
        self.site = Site.objects.create(
            name="Site Test",
            address="123 Test St"
        )
        
        self.equipment = Equipment.objects.create(
            name="Equipment Test",
            equipment_type="server",
            site=self.site,
            status="operational"
        )
    
    @patch.object(InfluxDBManager, 'write_data')
    def test_record_metric(self, mock_write):
        """Test de l'enregistrement d'une métrique"""
        mock_write.return_value = True
        
        result = self.service.record_metric(
            equipment_id=self.equipment.id,
            metric_type='temperature',
            value=25.5,
            tags={'location': 'room_a'}
        )
        
        self.assertTrue(result)
        mock_write.assert_called_once()
    
    @patch.object(InfluxDBManager, 'write_data')
    def test_record_availability(self, mock_write):
        """Test de l'enregistrement de la disponibilité"""
        mock_write.return_value = True
        
        result = self.service.record_availability(
            equipment_id=self.equipment.id,
            is_available=True,
            reason='operational'
        )
        
        self.assertTrue(result)
        mock_write.assert_called_once()
    
    @patch.object(InfluxDBManager, 'write_data')
    def test_record_performance(self, mock_write):
        """Test de l'enregistrement des performances"""
        mock_write.return_value = True
        
        result = self.service.record_performance(
            equipment_id=self.equipment.id,
            cpu_usage=45.2,
            memory_usage=62.8,
            response_time=120.5
        )
        
        self.assertTrue(result)
        self.assertEqual(mock_write.call_count, 3)  # 3 métriques


class EquipmentAnalyticsServiceTestCase(TestCase):
    """Tests pour le service d'analyse"""
    
    def setUp(self):
        self.service = EquipmentAnalyticsService()
        
        # Créer des données de test
        self.site = Site.objects.create(
            name="Site Test",
            address="123 Test St"
        )
        
        self.equipment = Equipment.objects.create(
            name="Equipment Test",
            equipment_type="server",
            site=self.site,
            status="operational"
        )
    
    @patch.object(InfluxDBManager, 'query_data')
    def test_get_equipment_metrics(self, mock_query):
        """Test de récupération des métriques"""
        # Simuler des données de retour
        mock_record = MagicMock()
        mock_record.get_time.return_value = datetime.now()
        mock_record.get_field.return_value = 'temperature'
        mock_record.get_value.return_value = 25.5
        mock_record.values = {'location': 'room_a'}
        
        mock_table = MagicMock()
        mock_table.records = [mock_record]
        
        mock_query.return_value = [mock_table]
        
        result = self.service.get_equipment_metrics(
            equipment_id=self.equipment.id,
            start_time=datetime.now() - timedelta(hours=1)
        )
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
    
    @patch.object(InfluxDBManager, 'query_data')
    def test_calculate_availability(self, mock_query):
        """Test du calcul de disponibilité"""
        # Simuler des données de disponibilité
        mock_records = []
        for i in range(10):
            mock_record = MagicMock()
            mock_record.get_value.return_value = 1 if i < 9 else 0  # 90% disponible
            mock_records.append(mock_record)
        
        mock_table = MagicMock()
        mock_table.records = mock_records
        
        mock_query.return_value = [mock_table]
        
        result = self.service.calculate_availability(
            equipment_id=self.equipment.id,
            start_time=datetime.now() - timedelta(days=1)
        )
        
        self.assertEqual(result, 90.0)


class InfluxDBViewsTestCase(TestCase):
    """Tests pour les vues API"""
    
    def setUp(self):
        self.client = Client()
        
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Créer des données de test
        self.site = Site.objects.create(
            name="Site Test",
            address="123 Test St"
        )
        
        self.equipment = Equipment.objects.create(
            name="Equipment Test",
            equipment_type="server",
            site=self.site,
            status="operational"
        )
        
        # Se connecter
        self.client.login(username='testuser', password='testpass123')
    
    @patch('influxdb_integration.views.EquipmentAnalyticsService')
    def test_equipment_metrics_view(self, mock_service):
        """Test de la vue des métriques d'équipement"""
        # Simuler le service
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        mock_instance.get_equipment_metrics.return_value = [
            {
                'time': '2024-01-01T10:00:00Z',
                'metric_type': 'temperature',
                'value': 25.5,
                'tags': {'location': 'room_a'}
            }
        ]
        
        url = reverse('equipment:equipment-metrics', kwargs={'pk': self.equipment.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('metrics', data)
        self.assertEqual(len(data['metrics']), 1)
    
    @patch('influxdb_integration.views.EquipmentAnalyticsService')
    def test_dashboard_view(self, mock_service):
        """Test de la vue du tableau de bord"""
        # Simuler le service
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        mock_instance.calculate_availability.return_value = 95.5
        mock_instance.get_performance_stats.return_value = {
            'cpu_avg': 45.2,
            'memory_avg': 62.8,
            'response_time_avg': 120.5
        }
        
        url = reverse('influxdb:dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('summary', data)
        self.assertIn('equipment_metrics', data)
    
    @patch('influxdb_integration.views.EquipmentAnalyticsService')
    def test_availability_report_view(self, mock_service):
        """Test de la vue du rapport de disponibilité"""
        # Simuler le service
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        mock_instance.calculate_availability.return_value = 98.5
        
        url = reverse('influxdb:availability-report')
        response = self.client.get(url, {
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('report', data)
        self.assertIn('period', data)


class SignalTestCase(TestCase):
    """Tests pour les signaux Django"""
    
    def setUp(self):
        # Créer des données de test
        self.site = Site.objects.create(
            name="Site Test",
            address="123 Test St"
        )
        
        self.equipment = Equipment.objects.create(
            name="Equipment Test",
            equipment_type="server",
            site=self.site,
            status="operational"
        )
    
    @patch('influxdb_integration.apps.metrics_service')
    def test_equipment_status_change_signal(self, mock_service):
        """Test du signal de changement de statut"""
        mock_service.record_metric.return_value = True
        mock_service.record_availability.return_value = True
        
        # Changer le statut
        self.equipment.status = 'maintenance'
        self.equipment.save()
        
        # Vérifier que les méthodes ont été appelées
        mock_service.record_metric.assert_called()
        mock_service.record_availability.assert_called()


class ManagementCommandTestCase(TestCase):
    """Tests pour les commandes de gestion"""
    
    def setUp(self):
        # Créer des données de test
        self.site = Site.objects.create(
            name="Site Test",
            address="123 Test St"
        )
        
        self.equipment = Equipment.objects.create(
            name="Equipment Test",
            equipment_type="server",
            site=self.site,
            status="operational"
        )
    
    @patch('influxdb_integration.management.commands.simulate_equipment_metrics.EquipmentMetricsService')
    def test_simulate_metrics_command(self, mock_service):
        """Test de la commande de simulation"""
        from django.core.management import call_command
        
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        
        # Exécuter la commande
        call_command('simulate_equipment_metrics', 
                    equipment_id=self.equipment.id,
                    duration=1)
        
        # Vérifier que des métriques ont été enregistrées
        self.assertTrue(mock_instance.record_performance.called)
        self.assertTrue(mock_instance.record_metric.called)