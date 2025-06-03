# 📚 BASE DE CONNAISSANCE - VIGILEOS BACKEND

## 🎯 Vue d'ensemble du projet

**VIGILEOS** est une application de surveillance et monitoring d'équipements réseau développée avec Django REST Framework. Le backend fournit une API REST complète pour gérer les entreprises, sites, équipements, alertes et métriques de performance.

## 🏗️ Architecture technique

### Stack technologique
- **Framework**: Django 4.2 + Django REST Framework
- **Base de données**: SQLite (dev) / PostgreSQL (prod)
- **Authentification**: JWT (JSON Web Tokens)
- **Documentation**: Swagger/OpenAPI
- **Filtrage**: django-filter
- **CORS**: django-cors-headers

### Structure du projet
```
backend/
├── vigileos/                 # Configuration principale Django
│   ├── settings/            # Paramètres par environnement
│   ├── urls.py             # URLs principales
│   └── views.py            # Vues globales (dashboard)
├── users/                   # App gestion utilisateurs/entreprises
├── sites/                   # App gestion sites
├── equipment/              # App gestion équipements
├── alerts/                 # App gestion alertes
├── metrics/                # App gestion métriques
├── create_test_data.py     # Script création données test
├── test_api.py            # Tests automatisés API
├── start.sh               # Script démarrage rapide
└── requirements.txt       # Dépendances Python
```

## 📊 Modèles de données

### 👥 Users App
- **User** (utilisateur étendu Django)
  - Profil avec entreprise, téléphone
  - Permissions par entreprise
  - Statut actif/inactif

- **Company** (entreprise)
  - Nom, adresse, date création
  - Relation avec utilisateurs et sites

### 🏢 Sites App
- **Site** (site géographique)
  - Nom, adresse, statut (active/online/offline/warning/pending)
  - Appartient à une entreprise
  - Contient des équipements

### 🖥️ Equipment App
- **Equipment** (équipement réseau)
  - Types: server, router, switch, camera, other
  - Statuts: online, offline, warning
  - Maintenance programmée
  - Appartient à un site

### 🚨 Alerts App
- **Alert** (alerte système)
  - Types: info, warning, error
  - Statuts: active, acknowledged, resolved
  - Liée à un équipement
  - Horodatage complet

- **AlertThreshold** (seuil d'alerte)
  - Seuils configurables par métrique
  - Valeurs min/max
  - Actions automatiques

### 📈 Metrics App
- **NetworkMetric** (métrique réseau)
  - CPU, mémoire, réseau, stockage
  - Horodatage précis
  - Liée à un équipement

## 🔌 API Endpoints

### 🔐 Authentification
```
POST /api/auth/login/          # Connexion JWT
POST /api/auth/register/       # Inscription
GET  /api/profile/             # Profil utilisateur
POST /api/change-password/     # Changement mot de passe
```

### 👥 Utilisateurs
```
GET    /api/users/             # Liste utilisateurs
POST   /api/users/             # Créer utilisateur
GET    /api/users/{id}/        # Détail utilisateur
PUT    /api/users/{id}/        # Modifier utilisateur
DELETE /api/users/{id}/        # Supprimer utilisateur
GET    /api/users/me/          # Mon profil
GET    /api/users/stats/       # Statistiques
```

### 🏢 Entreprises
```
GET    /api/companies/         # Liste entreprises
POST   /api/companies/         # Créer entreprise
GET    /api/companies/{id}/    # Détail entreprise
PUT    /api/companies/{id}/    # Modifier entreprise
GET    /api/companies/{id}/sites/    # Sites de l'entreprise
GET    /api/companies/{id}/stats/    # Statistiques entreprise
```

### 🏢 Sites
```
GET    /api/sites/             # Liste sites
POST   /api/sites/             # Créer site
GET    /api/sites/{id}/        # Détail site
GET    /api/sites/{id}/site_stats/   # Stats détaillées site
GET    /api/sites/{id}/equipment/    # Équipements du site
GET    /api/sites/{id}/alerts/       # Alertes du site
POST   /api/sites/{id}/set_status/   # Changer statut
GET    /api/sites/stats/       # Statistiques générales
GET    /api/sites/dashboard/   # Dashboard sites
```

### 🖥️ Équipements
```
GET    /api/equipment/         # Liste équipements
POST   /api/equipment/         # Créer équipement
GET    /api/equipment/{id}/    # Détail équipement
GET    /api/equipment/{id}/metrics/    # Métriques équipement
GET    /api/equipment/{id}/alerts/     # Alertes équipement
POST   /api/equipment/{id}/set_status/ # Changer statut
POST   /api/equipment/{id}/set_maintenance/ # Programmer maintenance
GET    /api/equipment/stats/   # Statistiques
GET    /api/equipment/by_type/ # Par type
GET    /api/equipment/maintenance_due/ # Maintenance due
```

### 🚨 Alertes
```
GET    /api/alerts/            # Liste alertes
POST   /api/alerts/            # Créer alerte
GET    /api/alerts/{id}/       # Détail alerte
POST   /api/alerts/{id}/acknowledge/ # Acquitter
POST   /api/alerts/{id}/resolve/     # Résoudre
GET    /api/alerts/active/     # Alertes actives
GET    /api/alerts/critical/   # Alertes critiques
GET    /api/alerts/stats/      # Statistiques
POST   /api/alerts/bulk_acknowledge/ # Acquitter en lot
```

### 📈 Métriques
```
GET    /api/metrics/           # Liste métriques
POST   /api/metrics/           # Créer métrique
GET    /api/metrics/latest/    # Dernières métriques
GET    /api/metrics/summary/   # Résumé
POST   /api/metrics/bulk_create/ # Création en lot
```

### 📊 Dashboard Global
```
GET    /api/dashboard/         # Dashboard complet avec toutes les stats
```

### 📚 Documentation
```
GET    /api/docs/              # Interface Swagger
GET    /api/schema/            # Schéma OpenAPI
```

## 🚀 Démarrage rapide

### 1. Installation
```bash
cd backend/
pip install -r requirements.txt
```

### 2. Configuration base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Données de test
```bash
python create_test_data.py
```

### 4. Démarrage serveur
```bash
./start.sh
# ou
python manage.py runserver 0.0.0.0:12000
```

### 5. Test de l'API
```bash
python test_api.py
```

## 🔑 Authentification

### Connexion
```bash
curl -X POST "http://localhost:12000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Utilisation du token
```bash
curl -X GET "http://localhost:12000/api/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Données de test créées

Le script `create_test_data.py` génère :
- **5 entreprises** avec adresses réalistes
- **5 utilisateurs** (admin/admin123, user1-4/password123)
- **15 sites** répartis dans les entreprises
- **37 équipements** de différents types
- **880 métriques** avec données historiques
- **11 seuils d'alerte** configurés
- **48 alertes** de différents types et statuts

## 🎛️ Fonctionnalités clés

### ✅ Implémenté et testé
- **Authentification JWT** complète
- **CRUD complet** sur tous les modèles
- **Filtrage avancé** avec django-filter
- **Pagination automatique** sur toutes les listes
- **Permissions par entreprise** (isolation des données)
- **Dashboard global** avec statistiques complètes
- **Opérations en lot** (bulk operations)
- **Gestion des statuts** équipements/sites
- **Système d'alertes** avec acquittement/résolution
- **Métriques temps réel** avec historique
- **Documentation Swagger** interactive
- **Health checks** pour monitoring
- **Tests automatisés** complets

### 🔧 Fonctionnalités avancées
- **Statistiques détaillées** par entité
- **Recherche textuelle** sur tous les endpoints
- **Tri configurable** sur tous les champs
- **Validation robuste** des données
- **Gestion d'erreurs** complète
- **Logs structurés** pour debugging
- **Optimisation requêtes** avec select_related
- **Cache intelligent** pour les statistiques

## 🧪 Tests et validation

### Tests automatisés
Le script `test_api.py` valide :
- ✅ Authentification JWT
- ✅ CRUD sur tous les modèles
- ✅ Filtrage et recherche
- ✅ Permissions et sécurité
- ✅ Dashboard et statistiques
- ✅ Opérations en lot
- ✅ Gestion des erreurs

### Résultats des tests
```
🚀 Démarrage des tests API VIGILEOS
✅ Connexion réussie pour admin
✅ 5 utilisateurs trouvés
✅ 5 entreprises trouvées
✅ 15 sites trouvés
✅ 37 équipements trouvés
✅ 48 alertes trouvées
✅ Dashboard global récupéré
✅ Tous les tests terminés avec succès!
```

## 🔗 Intégration Frontend

### URLs principales pour le frontend
- **Base API**: `http://localhost:12000/api/`
- **Authentification**: `/auth/login/`
- **Dashboard**: `/dashboard/`
- **Documentation**: `/docs/`

### Format des réponses
```json
{
  "count": 100,
  "next": "http://localhost:12000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

### Gestion des erreurs
```json
{
  "error": "Message d'erreur",
  "details": {...}
}
```

## 🚀 Prochaines étapes

### Pour l'intégration frontend
1. **Configurer les appels API** avec les endpoints documentés
2. **Implémenter l'authentification JWT** dans le frontend
3. **Créer les composants** pour chaque entité (users, companies, sites, equipment, alerts)
4. **Intégrer le dashboard** avec les statistiques temps réel
5. **Ajouter la gestion des permissions** selon l'entreprise de l'utilisateur

### Améliorations possibles
- **WebSockets** pour les notifications temps réel
- **Cache Redis** pour les performances
- **Elasticsearch** pour la recherche avancée
- **Celery** pour les tâches asynchrones
- **Monitoring avancé** avec Prometheus/Grafana

## 📞 Support et debugging

### Logs
```bash
tail -f server.log  # Logs du serveur Django
```

### Health checks
```bash
curl http://localhost:12000/api/health/
curl http://localhost:12000/api/readiness/
```

### Debug mode
Le serveur est configuré en mode DEBUG pour le développement avec des messages d'erreur détaillés.

---

## 🎉 Statut du projet

**✅ BACKEND COMPLET ET FONCTIONNEL**

Le backend VIGILEOS est maintenant :
- 🔐 **Sécurisé** avec authentification JWT
- 📊 **Complet** avec tous les modèles et endpoints
- 🧪 **Testé** avec validation automatisée
- 📚 **Documenté** avec Swagger
- 🚀 **Prêt** pour l'intégration frontend

**Prêt pour la phase de développement frontend !**