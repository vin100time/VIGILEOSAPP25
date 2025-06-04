# Guide de démarrage rapide - InfluxDB pour VIGILEOSAPP25

## 1. Configuration initiale

### Étape 1 : Copier le fichier d'environnement

```bash
cp .env.example .env
```

### Étape 2 : Vérifier les variables InfluxDB dans `.env`

```bash
# InfluxDB Configuration
INFLUXDB_URL=http://influxdb:8086
INFLUXDB_TOKEN=my-super-secret-auth-token
INFLUXDB_ORG=vigileos
INFLUXDB_BUCKET=equipment_metrics
INFLUXDB_USERNAME=admin
INFLUXDB_PASSWORD=secure_influx_password_123
```

### Étape 3 : Démarrer les services

```bash
docker-compose up -d
```

## 2. Vérification de l'installation

### Vérifier que InfluxDB est actif

```bash
docker-compose ps influxdb
```

### Accéder à l'interface InfluxDB

Ouvrez votre navigateur : http://localhost:8086

- Username : admin
- Password : secure_influx_password_123

## 3. Test rapide

### Simuler des métriques

```bash
docker-compose exec web python manage.py simulate_equipment_metrics --equipment-id=1 --duration=60
```

### Vérifier les métriques via l'API

```bash
curl -X GET "http://localhost:8000/api/influxdb/dashboard/"
```

## 4. Utilisation basique

### Dans le code Python

```python
from influxdb_integration.services import EquipmentMetricsService

# Enregistrer une métrique
service = EquipmentMetricsService()
service.record_metric(
    equipment_id=1,
    metric_type='temperature',
    value=25.5
)
```

### Via l'API REST

```bash
# Obtenir les métriques d'un équipement
curl -X GET "http://localhost:8000/api/equipment/1/metrics/"

# Obtenir le tableau de bord
curl -X GET "http://localhost:8000/api/influxdb/dashboard/"
```

## 5. Commandes utiles

```bash
# Voir les logs InfluxDB
docker-compose logs -f influxdb

# Redémarrer InfluxDB
docker-compose restart influxdb

# Exécuter des requêtes InfluxDB
docker exec -it vigileosapp-influxdb influx query 'from(bucket: "equipment_metrics") |> range(start: -1h)'
```

## 6. Dépannage rapide

### Erreur de connexion

1. Vérifier que InfluxDB est démarré :
   ```bash
   docker-compose ps influxdb
   ```

2. Vérifier les logs :
   ```bash
   docker-compose logs influxdb
   ```

3. Tester la connexion :
   ```bash
   docker-compose exec web python -c "from influxdb_integration.client import InfluxDBManager; print(InfluxDBManager().test_connection())"
   ```

### Pas de données

1. Vérifier qu'il y a des équipements :
   ```bash
   docker-compose exec web python manage.py shell -c "from equipment.models import Equipment; print(Equipment.objects.count())"
   ```

2. Simuler des données :
   ```bash
   docker-compose exec web python manage.py simulate_equipment_metrics --duration=300
   ```

## 7. Prochaines étapes

- Lire la [documentation complète](influxdb_integration.md)
- Explorer l'interface InfluxDB
- Configurer des alertes basées sur les métriques
- Créer des tableaux de bord personnalisés