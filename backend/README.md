# VIGILEOS Backend API

## Vue d'ensemble

Backend Django REST Framework complet pour l'application VIGILEOS - système de surveillance et monitoring d'équipements réseau.

## Architecture

### Applications Django

1. **users** - Gestion des utilisateurs et entreprises
2. **sites** - Gestion des sites
3. **equipment** - Gestion des équipements
4. **alerts** - Gestion des alertes
5. **metrics** - Gestion des métriques réseau

### Modèles de données

#### Users App
- **User** - Utilisateurs avec profils étendus
- **Company** - Entreprises clientes

#### Sites App
- **Site** - Sites géographiques des entreprises

#### Equipment App
- **Equipment** - Équipements réseau (serveurs, routeurs, switches, caméras)

#### Alerts App
- **Alert** - Alertes système
- **AlertThreshold** - Seuils d'alerte configurables

#### Metrics App
- **NetworkMetric** - Métriques de performance réseau

## API Endpoints

### Authentification
- `POST /api/auth/login/` - Connexion JWT
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/logout/` - Déconnexion
- `POST /api/auth/refresh/` - Renouvellement token
- `GET /api/profile/` - Profil utilisateur
- `POST /api/change-password/` - Changement mot de passe

### Utilisateurs
- `GET /api/users/` - Liste des utilisateurs
- `POST /api/users/` - Créer utilisateur
- `GET /api/users/{id}/` - Détail utilisateur
- `PUT/PATCH /api/users/{id}/` - Modifier utilisateur
- `DELETE /api/users/{id}/` - Supprimer utilisateur
- `GET /api/users/me/` - Profil utilisateur connecté
- `GET /api/users/stats/` - Statistiques utilisateurs
- `POST /api/users/{id}/activate/` - Activer utilisateur
- `POST /api/users/{id}/deactivate/` - Désactiver utilisateur

### Entreprises
- `GET /api/companies/` - Liste des entreprises
- `POST /api/companies/` - Créer entreprise
- `GET /api/companies/{id}/` - Détail entreprise
- `PUT/PATCH /api/companies/{id}/` - Modifier entreprise
- `DELETE /api/companies/{id}/` - Supprimer entreprise
- `GET /api/companies/my_company/` - Mon entreprise
- `GET /api/companies/{id}/sites/` - Sites de l'entreprise
- `GET /api/companies/{id}/users/` - Utilisateurs de l'entreprise
- `GET /api/companies/{id}/stats/` - Statistiques entreprise

### Sites
- `GET /api/sites/` - Liste des sites
- `POST /api/sites/` - Créer site
- `GET /api/sites/{id}/` - Détail site
- `PUT/PATCH /api/sites/{id}/` - Modifier site
- `DELETE /api/sites/{id}/` - Supprimer site
- `GET /api/sites/{id}/equipment/` - Équipements du site
- `GET /api/sites/{id}/alerts/` - Alertes du site
- `GET /api/sites/{id}/site_stats/` - Statistiques détaillées du site
- `POST /api/sites/{id}/set_status/` - Changer statut site
- `GET /api/sites/stats/` - Statistiques générales sites
- `GET /api/sites/dashboard/` - Dashboard sites
- `GET /api/sites/by_status/` - Sites par statut
- `GET /api/sites/pending/` - Sites en attente
- `GET /api/sites/with_alerts/` - Sites avec alertes
- `POST /api/sites/bulk_update/` - Mise à jour en lot

### Équipements
- `GET /api/equipment/` - Liste des équipements
- `POST /api/equipment/` - Créer équipement
- `GET /api/equipment/{id}/` - Détail équipement
- `PUT/PATCH /api/equipment/{id}/` - Modifier équipement
- `DELETE /api/equipment/{id}/` - Supprimer équipement
- `GET /api/equipment/{id}/metrics/` - Métriques de l'équipement
- `GET /api/equipment/{id}/alerts/` - Alertes de l'équipement
- `POST /api/equipment/{id}/set_status/` - Changer statut équipement
- `POST /api/equipment/{id}/set_maintenance/` - Programmer maintenance
- `GET /api/equipment/stats/` - Statistiques équipements
- `GET /api/equipment/dashboard/` - Dashboard équipements
- `GET /api/equipment/by_status/` - Équipements par statut
- `GET /api/equipment/by_type/` - Équipements par type
- `GET /api/equipment/maintenance_due/` - Équipements nécessitant maintenance
- `POST /api/equipment/bulk_update/` - Mise à jour en lot
- `POST /api/equipment/bulk_maintenance/` - Maintenance en lot

### Alertes
- `GET /api/alerts/` - Liste des alertes
- `POST /api/alerts/` - Créer alerte
- `GET /api/alerts/{id}/` - Détail alerte
- `PUT/PATCH /api/alerts/{id}/` - Modifier alerte
- `DELETE /api/alerts/{id}/` - Supprimer alerte
- `POST /api/alerts/{id}/acknowledge/` - Acquitter alerte
- `POST /api/alerts/{id}/resolve/` - Résoudre alerte
- `POST /api/alerts/{id}/reopen/` - Rouvrir alerte
- `GET /api/alerts/stats/` - Statistiques alertes
- `GET /api/alerts/dashboard/` - Dashboard alertes
- `GET /api/alerts/active/` - Alertes actives
- `GET /api/alerts/critical/` - Alertes critiques
- `GET /api/alerts/recent/` - Alertes récentes
- `POST /api/alerts/bulk_acknowledge/` - Acquitter en lot
- `POST /api/alerts/bulk_resolve/` - Résoudre en lot

### Métriques
- `GET /api/metrics/` - Liste des métriques
- `POST /api/metrics/` - Créer métrique
- `GET /api/metrics/{id}/` - Détail métrique
- `PUT/PATCH /api/metrics/{id}/` - Modifier métrique
- `DELETE /api/metrics/{id}/` - Supprimer métrique
- `GET /api/metrics/latest/` - Dernières métriques
- `GET /api/metrics/summary/` - Résumé métriques
- `POST /api/metrics/bulk_create/` - Création en lot

### Seuils d'alerte
- `GET /api/thresholds/` - Liste des seuils
- `POST /api/thresholds/` - Créer seuil
- `GET /api/thresholds/{id}/` - Détail seuil
- `PUT/PATCH /api/thresholds/{id}/` - Modifier seuil
- `DELETE /api/thresholds/{id}/` - Supprimer seuil
- `POST /api/thresholds/bulk_update/` - Mise à jour en lot

### Dashboard Global
- `GET /api/dashboard/` - Dashboard global avec toutes les statistiques

### Documentation
- `GET /api/docs/` - Documentation Swagger
- `GET /api/schema/` - Schéma OpenAPI

### Health Checks
- `GET /api/health/` - Vérification santé API
- `GET /api/readiness/` - Vérification disponibilité
- `GET /api/liveness/` - Vérification fonctionnement

## Fonctionnalités

### Authentification
- JWT (JSON Web Tokens)
- Gestion des permissions par entreprise
- Profils utilisateurs étendus

### Filtrage et recherche
- Filtres avancés avec django-filter
- Recherche textuelle
- Tri sur tous les endpoints

### Pagination
- Pagination automatique sur toutes les listes
- Paramètres configurables

### Permissions
- Isolation des données par entreprise
- Permissions granulaires
- Accès admin global

### Monitoring
- Métriques réseau en temps réel
- Alertes configurables
- Seuils personnalisables
- Dashboard complet

### Opérations en lot
- Mise à jour multiple
- Actions groupées
- Optimisation des performances

## Installation et démarrage

### Prérequis
```bash
pip install django djangorestframework django-filter djangorestframework-simplejwt django-cors-headers drf-spectacular
```

### Configuration
```bash
# Variables d'environnement
export DJANGO_SETTINGS_MODULE=vigileos.settings.development
export SECRET_KEY=your-secret-key
export DEBUG=True
```

### Base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### Données de test
```bash
python create_test_data.py
```

### Démarrage
```bash
python manage.py runserver 0.0.0.0:12000
```

## Tests

### Test complet de l'API
```bash
python test_api.py
```

### Tests unitaires Django
```bash
python manage.py test
```

## Données de test

Le script `create_test_data.py` crée :
- 5 entreprises
- 5 utilisateurs (admin/admin123)
- 15 sites
- 37 équipements
- 880 métriques
- 11 seuils d'alerte
- 48 alertes

## Structure des réponses

### Format standard
```json
{
  "count": 100,
  "next": "http://localhost:12000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

### Erreurs
```json
{
  "error": "Message d'erreur",
  "details": {...}
}
```

### Dashboard
```json
{
  "overview": {
    "total_companies": 5,
    "total_sites": 15,
    "total_equipment": 37,
    "total_users": 5,
    "total_alerts": 48,
    "active_alerts": 15,
    "critical_alerts": 16,
    "offline_equipment": 5,
    "maintenance_needed": 27
  },
  "equipment": {...},
  "alerts": {...},
  "sites": {...},
  "metrics": {...}
}
```

## Sécurité

- Authentification JWT obligatoire
- Isolation des données par entreprise
- Validation des entrées
- Protection CORS
- Logs d'audit

## Performance

- Optimisation des requêtes avec select_related/prefetch_related
- Pagination automatique
- Cache des statistiques
- Index sur les champs critiques

## Monitoring et logs

- Health checks intégrés
- Métriques de performance
- Logs structurés
- Alertes automatiques

## Déploiement

### Production
- Configuration HTTPS
- Base de données PostgreSQL
- Cache Redis
- Serveur WSGI (Gunicorn)
- Reverse proxy (Nginx)

### Docker
```dockerfile
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "vigileos.wsgi:application"]
```

## API Status

✅ **Complètement fonctionnel**
- Tous les endpoints implémentés
- Authentification JWT active
- Données de test créées
- Tests passent avec succès
- Documentation disponible
- Prêt pour intégration frontend