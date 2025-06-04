# Documentation InfluxDB pour VIGILEOSAPP25

## Table des matières

1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Installation et Configuration](#installation-et-configuration)
4. [Utilisation](#utilisation)
5. [API REST](#api-rest)
6. [Exemples de Code](#exemples-de-code)
7. [Métriques Collectées](#métriques-collectées)
8. [Tableaux de Bord](#tableaux-de-bord)
9. [Maintenance](#maintenance)
10. [Dépannage](#dépannage)

## Introduction

L'intégration InfluxDB dans VIGILEOSAPP25 permet de collecter, stocker et analyser les métriques temporelles des équipements. Cette solution offre :

- **Stockage optimisé** pour les données temporelles
- **Requêtes performantes** sur de grandes périodes
- **Agrégations automatiques** des données
- **Visualisations en temps réel**
- **Alertes basées sur les tendances**

## Architecture

### Composants principaux

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   Equipment     │────▶│   Django     │────▶│  InfluxDB   │
│   (Signals)     │     │  Integration │     │  Database   │
└─────────────────┘     └──────────────┘     └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   REST API   │
                        └──────────────┘
```

### Structure du module

```
backend/influxdb_integration/
├── __init__.py
├── apps.py              # Configuration Django
├── client.py            # Client InfluxDB
├── services.py          # Services métier
├── views.py             # API REST
├── urls.py              # Routes
└── management/
    └── commands/
        └── simulate_equipment_metrics.py
```

## Installation et Configuration

### 1. Variables d'environnement

Ajoutez ces variables dans votre fichier `.env` :

```bash
# InfluxDB Configuration
INFLUXDB_URL=http://influxdb:8086
INFLUXDB_TOKEN=my-super-secret-auth-token
INFLUXDB_ORG=vigileos
INFLUXDB_BUCKET=equipment_metrics
INFLUXDB_USERNAME=admin
INFLUXDB_PASSWORD=secure_influx_password_123
```

### 2. Docker Compose

Le service InfluxDB est déjà configuré dans `docker-compose.yml` :

```yaml
influxdb:
  image: influxdb:2.7-alpine
  container_name: vigileosapp-influxdb
  environment:
    DOCKER_INFLUXDB_INIT_MODE: setup
    DOCKER_INFLUXDB_INIT_USERNAME: ${INFLUXDB_USERNAME:-admin}
    DOCKER_INFLUXDB_INIT_PASSWORD: ${INFLUXDB_PASSWORD:-secure_influx_password_123}
    DOCKER_INFLUXDB_INIT_ORG: ${INFLUXDB_ORG:-vigileos}
    DOCKER_INFLUXDB_INIT_BUCKET: ${INFLUXDB_BUCKET:-equipment_metrics}
    DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: ${INFLUXDB_TOKEN:-my-super-secret-auth-token}
  volumes:
    - influxdb_data:/var/lib/influxdb2
    - influxdb_config:/etc/influxdb2
  ports:
    - "${INFLUXDB_PORT:-8086}:8086"
```

### 3. Démarrage

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier que InfluxDB est opérationnel
docker-compose ps influxdb

# Voir les logs
docker-compose logs influxdb
```

## Utilisation

### 1. Enregistrement automatique des métriques

Les métriques sont automatiquement enregistrées via les signaux Django :

```python
# Lors d'un changement de statut d'équipement
equipment = Equipment.objects.get(id=1)
equipment.status = 'maintenance'
equipment.save()  # Déclenche l'enregistrement dans InfluxDB
```

### 2. Enregistrement manuel

```python
from influxdb_integration.services import EquipmentMetricsService

# Créer une instance du service
metrics_service = EquipmentMetricsService()

# Enregistrer une métrique personnalisée
metrics_service.record_metric(
    equipment_id=1,
    metric_type='temperature',
    value=25.5,
    tags={'location': 'room_a', 'sensor': 'temp_01'}
)

# Enregistrer la disponibilité
metrics_service.record_availability(
    equipment_id=1,
    is_available=True,
    reason='operational'
)

# Enregistrer les performances
metrics_service.record_performance(
    equipment_id=1,
    cpu_usage=45.2,
    memory_usage=62.8,
    response_time=120.5
)
```

### 3. Consultation des métriques

```python
from influxdb_integration.services import EquipmentAnalyticsService
from datetime import datetime, timedelta

# Créer une instance du service d'analyse
analytics = EquipmentAnalyticsService()

# Obtenir les métriques des dernières 24h
end_time = datetime.now()
start_time = end_time - timedelta(days=1)

metrics = analytics.get_equipment_metrics(
    equipment_id=1,
    start_time=start_time,
    end_time=end_time
)

# Calculer la disponibilité
availability = analytics.calculate_availability(
    equipment_id=1,
    start_time=start_time,
    end_time=end_time
)
print(f"Disponibilité: {availability:.2f}%")

# Obtenir les statistiques de performance
perf_stats = analytics.get_performance_stats(
    equipment_id=1,
    start_time=start_time,
    end_time=end_time
)
```

## API REST

### Endpoints disponibles

#### 1. Métriques d'un équipement

```http
GET /api/equipment/{equipment_id}/metrics/
```

Paramètres de requête :
- `start_time` : Date de début (ISO 8601)
- `end_time` : Date de fin (ISO 8601)
- `metric_type` : Type de métrique (optionnel)

Exemple :
```bash
curl -X GET "http://localhost:8000/api/equipment/1/metrics/?start_time=2024-01-01T00:00:00Z&end_time=2024-01-02T00:00:00Z"
```

Réponse :
```json
{
  "equipment_id": 1,
  "metrics": [
    {
      "time": "2024-01-01T10:30:00Z",
      "metric_type": "temperature",
      "value": 25.5,
      "tags": {
        "location": "room_a",
        "sensor": "temp_01"
      }
    }
  ],
  "count": 150
}
```

#### 2. Tableau de bord des métriques

```http
GET /api/influxdb/dashboard/
```

Paramètres :
- `hours` : Nombre d'heures à afficher (défaut: 24)

Exemple :
```bash
curl -X GET "http://localhost:8000/api/influxdb/dashboard/?hours=48"
```

Réponse :
```json
{
  "summary": {
    "total_equipment": 25,
    "operational": 20,
    "maintenance": 3,
    "offline": 2,
    "average_availability": 92.5
  },
  "equipment_metrics": [
    {
      "equipment_id": 1,
      "name": "Serveur Principal",
      "current_status": "operational",
      "availability_24h": 98.5,
      "last_metric": "2024-01-02T15:30:00Z",
      "performance": {
        "cpu_avg": 45.2,
        "memory_avg": 62.8,
        "response_time_avg": 120.5
      }
    }
  ]
}
```

#### 3. Rapport de disponibilité

```http
GET /api/influxdb/availability-report/
```

Paramètres :
- `start_date` : Date de début (YYYY-MM-DD)
- `end_date` : Date de fin (YYYY-MM-DD)
- `equipment_id` : ID de l'équipement (optionnel)

Exemple :
```bash
curl -X GET "http://localhost:8000/api/influxdb/availability-report/?start_date=2024-01-01&end_date=2024-01-31"
```

## Exemples de Code

### 1. Script de monitoring

```python
# monitoring_script.py
from influxdb_integration.services import EquipmentMetricsService
from equipment.models import Equipment
import psutil
import time

def monitor_equipment():
    """Surveille les équipements et enregistre les métriques"""
    metrics_service = EquipmentMetricsService()
    
    while True:
        for equipment in Equipment.objects.filter(status='operational'):
            # Simuler la collecte de métriques
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            
            # Enregistrer les performances
            metrics_service.record_performance(
                equipment_id=equipment.id,
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                response_time=100  # ms
            )
            
        time.sleep(60)  # Attendre 1 minute

if __name__ == "__main__":
    monitor_equipment()
```

### 2. Génération de rapports

```python
# generate_report.py
from influxdb_integration.services import EquipmentAnalyticsService
from datetime import datetime, timedelta
import pandas as pd

def generate_monthly_report():
    """Génère un rapport mensuel de disponibilité"""
    analytics = EquipmentAnalyticsService()
    
    # Période du rapport
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    # Collecter les données
    report_data = []
    
    for equipment in Equipment.objects.all():
        availability = analytics.calculate_availability(
            equipment_id=equipment.id,
            start_time=start_time,
            end_time=end_time
        )
        
        stats = analytics.get_performance_stats(
            equipment_id=equipment.id,
            start_time=start_time,
            end_time=end_time
        )
        
        report_data.append({
            'Equipment': equipment.name,
            'Type': equipment.equipment_type,
            'Availability (%)': availability,
            'Avg CPU (%)': stats.get('cpu_avg', 0),
            'Avg Memory (%)': stats.get('memory_avg', 0),
            'Avg Response Time (ms)': stats.get('response_time_avg', 0)
        })
    
    # Créer un DataFrame
    df = pd.DataFrame(report_data)
    
    # Sauvegarder en Excel
    df.to_excel(f'report_{start_time.strftime("%Y-%m")}.xlsx', index=False)
    
    return df

if __name__ == "__main__":
    report = generate_monthly_report()
    print(report)
```

### 3. Alertes basées sur les tendances

```python
# trend_alerts.py
from influxdb_integration.services import EquipmentAnalyticsService
from alerts.models import Alert
from datetime import datetime, timedelta

def check_performance_trends():
    """Vérifie les tendances de performance et crée des alertes"""
    analytics = EquipmentAnalyticsService()
    
    for equipment in Equipment.objects.filter(status='operational'):
        # Analyser les 7 derniers jours
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        stats = analytics.get_performance_stats(
            equipment_id=equipment.id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Vérifier les seuils
        if stats.get('cpu_avg', 0) > 80:
            Alert.objects.create(
                equipment=equipment,
                alert_type='performance',
                severity='warning',
                message=f"CPU usage élevé: {stats['cpu_avg']:.1f}% en moyenne sur 7 jours"
            )
        
        if stats.get('memory_avg', 0) > 90:
            Alert.objects.create(
                equipment=equipment,
                alert_type='performance',
                severity='critical',
                message=f"Mémoire critique: {stats['memory_avg']:.1f}% en moyenne"
            )

if __name__ == "__main__":
    check_performance_trends()
```

## Métriques Collectées

### 1. Métriques de statut

- **status_change** : Changement d'état de l'équipement
  - Tags : `previous_status`, `new_status`
  - Valeur : 1 (événement)

### 2. Métriques de disponibilité

- **availability** : État de disponibilité
  - Tags : `reason`
  - Valeur : 1 (disponible) ou 0 (indisponible)

### 3. Métriques de performance

- **cpu_usage** : Utilisation CPU en pourcentage
- **memory_usage** : Utilisation mémoire en pourcentage
- **response_time** : Temps de réponse en millisecondes

### 4. Métriques personnalisées

- **temperature** : Température en degrés Celsius
- **power_consumption** : Consommation électrique en watts
- **network_traffic** : Trafic réseau en bytes/s

## Tableaux de Bord

### 1. Vue d'ensemble

Le tableau de bord principal affiche :
- Nombre total d'équipements
- Répartition par statut
- Disponibilité moyenne
- Alertes récentes

### 2. Détail par équipement

Pour chaque équipement :
- Graphique de disponibilité sur 24h
- Courbes de performance (CPU, mémoire)
- Historique des changements de statut
- Métriques personnalisées

### 3. Rapports

- Rapport de disponibilité mensuel
- Analyse des tendances
- Comparaison entre équipements
- Export PDF/Excel

## Maintenance

### 1. Rétention des données

Configuration de la rétention dans InfluxDB :

```bash
# Se connecter au conteneur InfluxDB
docker exec -it vigileosapp-influxdb influx

# Créer une politique de rétention (30 jours)
CREATE RETENTION POLICY "30days" ON "equipment_metrics" DURATION 30d REPLICATION 1 DEFAULT
```

### 2. Sauvegarde

```bash
# Sauvegarder les données InfluxDB
docker exec vigileosapp-influxdb influx backup /backup/$(date +%Y%m%d)

# Copier la sauvegarde localement
docker cp vigileosapp-influxdb:/backup ./influxdb-backups/
```

### 3. Optimisation

```python
# Commande Django pour optimiser les données
python manage.py optimize_influxdb_data --days=7
```

## Dépannage

### 1. Problèmes de connexion

```python
# Tester la connexion
from influxdb_integration.client import InfluxDBManager

manager = InfluxDBManager()
if manager.test_connection():
    print("Connexion OK")
else:
    print("Erreur de connexion")
```

### 2. Vérifier les logs

```bash
# Logs InfluxDB
docker-compose logs influxdb

# Logs Django
docker-compose logs web | grep influxdb
```

### 3. Requêtes de débogage

```python
# Requête directe InfluxDB
from influxdb_integration.client import InfluxDBManager

manager = InfluxDBManager()
query = '''
from(bucket: "equipment_metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "equipment_metrics")
  |> limit(n: 10)
'''
results = manager.query_data(query)
for table in results:
    for record in table.records:
        print(f"{record.get_time()}: {record.get_field()} = {record.get_value()}")
```

### 4. Commandes utiles

```bash
# Simuler des métriques pour tester
python manage.py simulate_equipment_metrics --equipment-id=1 --duration=60

# Vérifier l'état du service
docker-compose exec web python manage.py check_influxdb_status

# Nettoyer les anciennes données
python manage.py cleanup_influxdb_data --older-than=90
```

## Intégration avec l'application

### 1. Dans les vues Django

```python
from django.shortcuts import render
from influxdb_integration.services import EquipmentAnalyticsService

def equipment_detail_view(request, equipment_id):
    analytics = EquipmentAnalyticsService()
    
    # Obtenir les métriques des dernières 24h
    metrics = analytics.get_equipment_metrics(
        equipment_id=equipment_id,
        start_time=datetime.now() - timedelta(hours=24)
    )
    
    context = {
        'equipment': Equipment.objects.get(id=equipment_id),
        'metrics': metrics,
        'availability': analytics.calculate_availability(equipment_id)
    }
    
    return render(request, 'equipment/detail.html', context)
```

### 2. Dans les tâches Celery

```python
from celery import shared_task
from influxdb_integration.services import EquipmentMetricsService

@shared_task
def collect_equipment_metrics():
    """Tâche périodique pour collecter les métriques"""
    metrics_service = EquipmentMetricsService()
    
    for equipment in Equipment.objects.filter(status='operational'):
        # Collecter et enregistrer les métriques
        metrics_service.record_performance(
            equipment_id=equipment.id,
            cpu_usage=get_cpu_usage(equipment),
            memory_usage=get_memory_usage(equipment),
            response_time=get_response_time(equipment)
        )
```

### 3. WebSocket pour temps réel

```python
# consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from influxdb_integration.services import EquipmentMetricsService

class MetricsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.equipment_id = self.scope['url_route']['kwargs']['equipment_id']
        await self.accept()
        
        # Envoyer les métriques en temps réel
        await self.send_metrics()
    
    async def send_metrics(self):
        metrics_service = EquipmentMetricsService()
        while True:
            metrics = await metrics_service.get_latest_metrics(self.equipment_id)
            await self.send_json(metrics)
            await asyncio.sleep(5)  # Mise à jour toutes les 5 secondes
```

## Conclusion

L'intégration InfluxDB dans VIGILEOSAPP25 offre une solution robuste et performante pour le suivi des équipements. Elle permet :

- Un stockage efficace des données temporelles
- Des analyses en temps réel
- Des rapports détaillés
- Une base solide pour l'IA prédictive

Pour toute question ou amélioration, consultez la documentation InfluxDB officielle ou contactez l'équipe de développement.