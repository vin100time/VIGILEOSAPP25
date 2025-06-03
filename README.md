# VIGILEOSAPP25 🚀

Application de surveillance réseau et monitoring d'infrastructure développée avec Django REST Framework et React.

## 📋 Table des matières

- [Aperçu](#aperçu)
- [Architecture](#architecture)
- [Installation rapide](#installation-rapide)
- [Développement](#développement)
- [Production](#production)
- [API Documentation](#api-documentation)
- [Monitoring](#monitoring)
- [Contribution](#contribution)

## 🎯 Aperçu

VIGILEOSAPP25 est une solution complète de surveillance réseau qui permet de :

- 📊 Monitorer les équipements réseau en temps réel
- 🚨 Gérer les alertes et notifications
- 📈 Analyser les métriques de performance
- 🏢 Organiser les sites et équipements
- 👥 Gérer les utilisateurs et permissions

### Technologies utilisées

**Backend:**
- Django 4.2 + Django REST Framework
- PostgreSQL 15 avec optimisations time-series
- Redis pour le cache et les tâches asynchrones
- Celery pour les tâches en arrière-plan
- Docker pour la containerisation

**Frontend:**
- React 18 avec TypeScript
- Material-UI pour l'interface
- Axios pour les appels API
- Chart.js pour les graphiques

**Infrastructure:**
- Nginx comme reverse proxy
- Docker Compose pour l'orchestration
- SSL/TLS avec certificats automatiques
- Monitoring avec health checks

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Nginx         │    │   Backend       │
│   React         │◄──►│   Reverse Proxy │◄──►│   Django        │
│   Port 3000     │    │   Port 80/443   │    │   Port 8000     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐             │
                       │   Celery        │◄────────────┤
                       │   Workers       │             │
                       │                 │             │
                       └─────────────────┘             │
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│   PostgreSQL    │◄───│   Redis         │◄────────────┘
│   Database      │    │   Cache/Queue   │
│   Port 5432     │    │   Port 6379     │
└─────────────────┘    └─────────────────┘
```

## ⚡ Installation rapide

### Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Installation en une commande

```bash
# Cloner le projet
git clone https://github.com/vin100time/VIGILEOSAPP25.git
cd VIGILEOSAPP25

# Installation et démarrage automatique
make install
```

L'application sera disponible sur :
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
- **Documentation API**: http://localhost:8000/api/docs
- **MailHog** (emails de test): http://localhost:8025

### Connexion par défaut

- **Utilisateur**: admin
- **Mot de passe**: admin123

## 🛠️ Développement

### Commandes principales

```bash
# Démarrer l'environnement de développement
make dev-start

# Voir les logs en temps réel
make dev-logs

# Accéder au shell Django
make dev-shell

# Exécuter les migrations
make dev-migrate

# Créer de nouvelles migrations
make dev-makemigrations

# Exécuter les tests
make dev-test

# Arrêter les services
make dev-stop

# Nettoyer l'environnement
make dev-clean
```

### Structure du projet

```
VIGILEOSAPP25/
├── backend/                 # Application Django
│   ├── vigileos/           # Configuration principale
│   ├── users/              # Gestion des utilisateurs
│   ├── sites/              # Gestion des sites
│   ├── equipment/          # Gestion des équipements
│   ├── alerts/             # Système d'alertes
│   ├── metrics/            # Métriques et monitoring
│   └── requirements/       # Dépendances Python
├── frontend/               # Application React
│   ├── src/
│   ├── public/
│   └── package.json
├── docker/                 # Configuration Docker
│   ├── nginx/              # Configuration Nginx
│   ├── postgres/           # Configuration PostgreSQL
│   └── redis/              # Configuration Redis
├── scripts/                # Scripts de déploiement
├── docker-compose.yml      # Production
├── docker-compose.dev.yml  # Développement
└── Makefile               # Commandes simplifiées
```

### Variables d'environnement

Copiez `.env.example` vers `.env` et modifiez selon vos besoins :

```bash
cp .env.example .env
```

Variables principales :
- `DEBUG`: Mode debug (True/False)
- `SECRET_KEY`: Clé secrète Django
- `DATABASE_URL`: URL de la base de données
- `REDIS_URL`: URL du cache Redis
- `ALLOWED_HOSTS`: Hosts autorisés

### Développement de l'API

L'API suit les conventions REST et utilise Django REST Framework :

```python
# Exemple d'endpoint
GET /api/sites/                 # Liste des sites
POST /api/sites/                # Créer un site
GET /api/sites/{id}/            # Détail d'un site
PUT /api/sites/{id}/            # Modifier un site
DELETE /api/sites/{id}/         # Supprimer un site
```

Documentation interactive disponible sur `/api/docs/`

## 🚀 Production

### Déploiement

```bash
# Configuration pour la production
make prod-setup

# Modifier le fichier .env avec vos vraies valeurs
nano .env

# Déploiement complet
make prod-deploy
```

### Configuration SSL

Pour la production, placez vos certificats SSL dans `docker/ssl/` :
- `cert.pem` : Certificat SSL
- `key.pem` : Clé privée

### Scaling horizontal

```bash
# Augmenter le nombre d'instances web
docker-compose up -d --scale web=3

# Ou via le script de déploiement
./scripts/deploy.sh production scale web=3
```

### Sauvegarde

```bash
# Sauvegarde automatique
make backup

# Restauration
make restore BACKUP=backups/postgres_backup_20231201_120000.sql.gz
```

## 📊 Monitoring

### Health Checks

L'application expose plusieurs endpoints de santé :

- `/health/` : Check simple pour load balancers
- `/api/health/` : Check complet avec détails des services
- `/api/readiness/` : Vérification de disponibilité
- `/api/liveness/` : Vérification de vie

### Logs

```bash
# Logs en temps réel
make logs

# Logs d'un service spécifique
docker-compose logs -f web

# Logs avec horodatage
docker-compose logs -f -t
```

### Métriques

Les métriques sont collectées automatiquement :
- Performance des requêtes PostgreSQL
- Utilisation du cache Redis
- Métriques applicatives Django
- Métriques système via Docker

## 🔧 Configuration avancée

### PostgreSQL

Configuration optimisée pour les time-series dans `docker/postgres/postgresql.conf` :
- Shared buffers : 256MB
- Work mem : 4MB
- Autovacuum optimisé
- Extensions : uuid-ossp, pg_trgm, btree_gin

### Redis

Configuration pour Django et Celery dans `docker/redis/redis.conf` :
- Maxmemory : 512MB
- Policy : allkeys-lru
- Persistance : AOF + RDB
- Bases séparées par usage

### Nginx

Configuration haute performance dans `docker/nginx/` :
- Compression gzip
- Cache statique
- Rate limiting
- Headers de sécurité
- Support WebSocket

## 🧪 Tests

```bash
# Tests unitaires
make test

# Tests avec coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report

# Tests d'intégration
docker-compose exec web python manage.py test --tag=integration
```

## 📚 API Documentation

### Authentification

L'API utilise l'authentification par token JWT :

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Utiliser le token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/sites/
```

### Endpoints principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/auth/` | POST | Authentification |
| `/api/sites/` | GET, POST | Gestion des sites |
| `/api/equipment/` | GET, POST | Gestion des équipements |
| `/api/alerts/` | GET, POST | Gestion des alertes |
| `/api/metrics/` | GET, POST | Métriques de monitoring |

Documentation complète : http://localhost:8000/api/docs/

## 🤝 Contribution

### Workflow de développement

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

### Standards de code

- **Python** : PEP 8, Black formatter
- **JavaScript** : ESLint, Prettier
- **Commits** : Convention Conventional Commits
- **Tests** : Coverage minimum 80%

### Environnement de développement

```bash
# Installation des hooks pre-commit
pip install pre-commit
pre-commit install

# Vérification du code
make lint

# Tests avant commit
make test
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

- **Documentation** : [Wiki du projet](https://github.com/vin100time/VIGILEOSAPP25/wiki)
- **Issues** : [GitHub Issues](https://github.com/vin100time/VIGILEOSAPP25/issues)
- **Discussions** : [GitHub Discussions](https://github.com/vin100time/VIGILEOSAPP25/discussions)

## 🎉 Remerciements

- Django et Django REST Framework
- React et l'écosystème JavaScript
- PostgreSQL et Redis
- Docker et Docker Compose
- Nginx
- Toute la communauté open source

---

**VIGILEOSAPP25** - Surveillance réseau moderne et scalable 🚀 