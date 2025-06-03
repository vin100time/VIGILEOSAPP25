# VIGILEOSAPP25 - Documentation API

## 📋 Vue d'ensemble

L'API VIGILEOSAPP25 est une API REST construite avec Django REST Framework qui fournit des endpoints pour la gestion de la surveillance réseau et du monitoring d'infrastructure.

## 🔗 URL de base

- **Développement**: `http://localhost:8000/api/`
- **Production**: `https://votre-domaine.com/api/`

## 🔐 Authentification

L'API utilise l'authentification par token JWT (JSON Web Token).

### Obtenir un token

```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "votre_username",
    "password": "votre_password"
}
```

**Réponse:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

### Utiliser le token

Incluez le token dans l'en-tête Authorization de vos requêtes :

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Rafraîchir le token

```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 📊 Endpoints principaux

### 🏢 Sites

#### Lister tous les sites

```http
GET /api/sites/
Authorization: Bearer <token>
```

**Paramètres de requête:**
- `page` (int): Numéro de page (défaut: 1)
- `page_size` (int): Nombre d'éléments par page (défaut: 20)
- `search` (string): Recherche par nom ou description
- `company` (int): Filtrer par ID de l'entreprise

**Réponse:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/sites/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Site Principal",
            "description": "Site principal de l'entreprise",
            "address": "123 Rue de la Paix, Paris",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "company": 1,
            "created_at": "2023-12-01T10:00:00Z",
            "updated_at": "2023-12-01T10:00:00Z",
            "equipment_count": 15,
            "active_alerts_count": 2
        }
    ]
}
```

#### Créer un site

```http
POST /api/sites/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Nouveau Site",
    "description": "Description du nouveau site",
    "address": "456 Avenue des Champs, Lyon",
    "latitude": 45.7640,
    "longitude": 4.8357,
    "company": 1
}
```

#### Obtenir un site spécifique

```http
GET /api/sites/{id}/
Authorization: Bearer <token>
```

#### Mettre à jour un site

```http
PUT /api/sites/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Site Modifié",
    "description": "Description mise à jour"
}
```

#### Supprimer un site

```http
DELETE /api/sites/{id}/
Authorization: Bearer <token>
```

### 🖥️ Équipements

#### Lister tous les équipements

```http
GET /api/equipment/
Authorization: Bearer <token>
```

**Paramètres de requête:**
- `site` (int): Filtrer par ID du site
- `type` (string): Filtrer par type d'équipement
- `status` (string): Filtrer par statut (online, offline, maintenance)
- `search` (string): Recherche par nom ou adresse IP

**Réponse:**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/equipment/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Routeur Principal",
            "type": "router",
            "ip_address": "192.168.1.1",
            "mac_address": "00:11:22:33:44:55",
            "status": "online",
            "site": 1,
            "manufacturer": "Cisco",
            "model": "ISR4331",
            "serial_number": "ABC123456",
            "firmware_version": "16.09.04",
            "last_seen": "2023-12-01T15:30:00Z",
            "created_at": "2023-12-01T10:00:00Z",
            "updated_at": "2023-12-01T15:30:00Z"
        }
    ]
}
```

#### Créer un équipement

```http
POST /api/equipment/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Nouveau Switch",
    "type": "switch",
    "ip_address": "192.168.1.10",
    "mac_address": "00:11:22:33:44:66",
    "site": 1,
    "manufacturer": "HP",
    "model": "ProCurve 2920"
}
```

### 🚨 Alertes

#### Lister toutes les alertes

```http
GET /api/alerts/
Authorization: Bearer <token>
```

**Paramètres de requête:**
- `severity` (string): Filtrer par sévérité (low, medium, high, critical)
- `status` (string): Filtrer par statut (open, acknowledged, resolved)
- `equipment` (int): Filtrer par ID de l'équipement
- `site` (int): Filtrer par ID du site
- `date_from` (date): Date de début (format: YYYY-MM-DD)
- `date_to` (date): Date de fin (format: YYYY-MM-DD)

**Réponse:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Équipement hors ligne",
            "description": "Le routeur principal ne répond plus",
            "severity": "high",
            "status": "open",
            "equipment": 1,
            "site": 1,
            "created_at": "2023-12-01T16:00:00Z",
            "updated_at": "2023-12-01T16:00:00Z",
            "acknowledged_at": null,
            "resolved_at": null,
            "acknowledged_by": null
        }
    ]
}
```

#### Créer une alerte

```http
POST /api/alerts/
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Nouvelle alerte",
    "description": "Description de l'alerte",
    "severity": "medium",
    "equipment": 1
}
```

#### Acquitter une alerte

```http
POST /api/alerts/{id}/acknowledge/
Authorization: Bearer <token>
```

#### Résoudre une alerte

```http
POST /api/alerts/{id}/resolve/
Authorization: Bearer <token>
Content-Type: application/json

{
    "resolution_note": "Problème résolu en redémarrant l'équipement"
}
```

### 📈 Métriques

#### Lister les métriques

```http
GET /api/metrics/
Authorization: Bearer <token>
```

**Paramètres de requête:**
- `equipment` (int): Filtrer par ID de l'équipement
- `metric_type` (string): Type de métrique (cpu, memory, network, disk)
- `date_from` (datetime): Date de début (format: YYYY-MM-DDTHH:MM:SS)
- `date_to` (datetime): Date de fin (format: YYYY-MM-DDTHH:MM:SS)
- `aggregation` (string): Type d'agrégation (avg, min, max, sum)
- `interval` (string): Intervalle d'agrégation (1m, 5m, 1h, 1d)

**Réponse:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/metrics/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "equipment": 1,
            "metric_type": "cpu",
            "value": 75.5,
            "unit": "percent",
            "timestamp": "2023-12-01T16:00:00Z",
            "metadata": {
                "core_count": 4,
                "load_average": 2.1
            }
        }
    ]
}
```

#### Ajouter des métriques

```http
POST /api/metrics/
Authorization: Bearer <token>
Content-Type: application/json

{
    "equipment": 1,
    "metric_type": "memory",
    "value": 8192,
    "unit": "MB",
    "metadata": {
        "used": 6144,
        "free": 2048
    }
}
```

#### Obtenir des statistiques agrégées

```http
GET /api/metrics/stats/
Authorization: Bearer <token>
```

**Paramètres de requête:**
- `equipment` (int): ID de l'équipement
- `metric_type` (string): Type de métrique
- `period` (string): Période (1h, 24h, 7d, 30d)

**Réponse:**
```json
{
    "equipment": 1,
    "metric_type": "cpu",
    "period": "24h",
    "stats": {
        "avg": 65.2,
        "min": 12.5,
        "max": 98.7,
        "count": 1440,
        "trend": "increasing"
    },
    "data_points": [
        {
            "timestamp": "2023-12-01T00:00:00Z",
            "value": 45.2
        }
    ]
}
```

### 👥 Utilisateurs

#### Profil utilisateur

```http
GET /api/auth/profile/
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_staff": true,
    "is_superuser": true,
    "date_joined": "2023-12-01T10:00:00Z",
    "last_login": "2023-12-01T16:00:00Z",
    "company": {
        "id": 1,
        "name": "Mon Entreprise"
    }
}
```

#### Mettre à jour le profil

```http
PUT /api/auth/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "Nouveau Prénom",
    "last_name": "Nouveau Nom",
    "email": "nouveau@email.com"
}
```

#### Changer le mot de passe

```http
POST /api/auth/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
    "old_password": "ancien_mot_de_passe",
    "new_password": "nouveau_mot_de_passe"
}
```

## 🔍 Monitoring et Santé

### Vérification de santé

```http
GET /api/health/
```

**Réponse:**
```json
{
    "status": "healthy",
    "timestamp": 1701442800,
    "services": {
        "database": {
            "status": "healthy",
            "type": "postgresql",
            "response_time_ms": 12.5
        },
        "cache": {
            "status": "healthy",
            "type": "redis",
            "response_time_ms": 3.2
        },
        "celery": {
            "status": "healthy",
            "type": "task_queue",
            "workers": 2,
            "response_time_ms": 8.7
        }
    },
    "version": "1.0.0",
    "environment": "production",
    "response_time_ms": 25.4
}
```

### Vérification de disponibilité

```http
GET /api/readiness/
```

### Vérification de vie

```http
GET /api/liveness/
```

## 📝 Codes de statut HTTP

| Code | Signification | Description |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 204 | No Content | Requête réussie sans contenu de réponse |
| 400 | Bad Request | Données de requête invalides |
| 401 | Unauthorized | Authentification requise |
| 403 | Forbidden | Permissions insuffisantes |
| 404 | Not Found | Ressource non trouvée |
| 409 | Conflict | Conflit avec l'état actuel de la ressource |
| 422 | Unprocessable Entity | Données valides mais non traitables |
| 429 | Too Many Requests | Limite de taux dépassée |
| 500 | Internal Server Error | Erreur serveur interne |
| 503 | Service Unavailable | Service temporairement indisponible |

## 🚫 Gestion des erreurs

### Format des erreurs

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Les données fournies ne sont pas valides",
        "details": {
            "name": ["Ce champ est requis."],
            "ip_address": ["Adresse IP invalide."]
        },
        "timestamp": "2023-12-01T16:00:00Z"
    }
}
```

### Codes d'erreur courants

| Code | Description |
|------|-------------|
| `AUTHENTICATION_FAILED` | Échec de l'authentification |
| `PERMISSION_DENIED` | Permissions insuffisantes |
| `VALIDATION_ERROR` | Erreur de validation des données |
| `NOT_FOUND` | Ressource non trouvée |
| `RATE_LIMIT_EXCEEDED` | Limite de taux dépassée |
| `SERVER_ERROR` | Erreur serveur interne |

## 📊 Pagination

Toutes les listes d'objets sont paginées par défaut.

### Paramètres de pagination

- `page`: Numéro de page (défaut: 1)
- `page_size`: Nombre d'éléments par page (défaut: 20, max: 100)

### Format de réponse paginée

```json
{
    "count": 150,
    "next": "http://localhost:8000/api/sites/?page=3",
    "previous": "http://localhost:8000/api/sites/?page=1",
    "results": [...]
}
```

## 🔍 Filtrage et recherche

### Filtres disponibles

La plupart des endpoints supportent le filtrage via des paramètres de requête :

```http
GET /api/equipment/?site=1&status=online&type=router
```

### Recherche textuelle

Utilisez le paramètre `search` pour la recherche textuelle :

```http
GET /api/sites/?search=paris
```

### Tri

Utilisez le paramètre `ordering` pour trier les résultats :

```http
GET /api/alerts/?ordering=-created_at
```

Préfixez avec `-` pour un tri décroissant.

## 📅 Formats de date

Toutes les dates sont au format ISO 8601 en UTC :

- **DateTime**: `2023-12-01T16:00:00Z`
- **Date**: `2023-12-01`
- **Time**: `16:00:00`

## 🔒 Limites de taux

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| `/api/auth/login/` | 5 requêtes | 1 minute |
| `/api/` (général) | 100 requêtes | 1 minute |
| `/api/metrics/` | 1000 requêtes | 1 minute |

## 📚 Exemples d'utilisation

### Python avec requests

```python
import requests

# Authentification
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['access']

# Utilisation de l'API
headers = {'Authorization': f'Bearer {token}'}
sites = requests.get('http://localhost:8000/api/sites/', headers=headers)
print(sites.json())
```

### JavaScript avec fetch

```javascript
// Authentification
const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
});
const { access: token } = await response.json();

// Utilisation de l'API
const sites = await fetch('http://localhost:8000/api/sites/', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
const sitesData = await sites.json();
console.log(sitesData);
```

### cURL

```bash
# Authentification
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}' | \
    jq -r '.access')

# Utilisation de l'API
curl -H "Authorization: Bearer $TOKEN" \
    http://localhost:8000/api/sites/
```

## 🔄 Webhooks (Futur)

Les webhooks permettront de recevoir des notifications en temps réel pour certains événements :

- Création/modification d'alertes
- Changement de statut d'équipement
- Seuils de métriques dépassés

## 📖 Documentation interactive

La documentation interactive Swagger/OpenAPI est disponible à :

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **Schéma OpenAPI**: `http://localhost:8000/api/schema/`

## 🆘 Support

Pour toute question ou problème avec l'API :

1. Consultez cette documentation
2. Vérifiez les logs de l'application
3. Créez une issue sur le dépôt GitHub
4. Contactez l'équipe de développement

---

**Version de l'API**: 1.0.0  
**Dernière mise à jour**: Décembre 2023