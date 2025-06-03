# Base de Connaissance - Projet Vigileos

## Vue d'ensemble du projet

Vigileos est une application web de surveillance d'équipements et de sites pour différentes entreprises. Le projet utilise une architecture moderne avec un frontend React/TypeScript et un backend Django REST API.

## Architecture générale

### Stack technique
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Backend**: Django 4.2 + Django REST Framework + PostgreSQL
- **Authentification**: JWT (JSON Web Tokens)
- **Containerisation**: Docker + Docker Compose
- **Base de données**: PostgreSQL

### Structure du projet
```
VIGILEOSAPP25/
├── frontend/                 # Application React TypeScript
│   ├── src/
│   │   ├── components/      # Composants réutilisables
│   │   ├── pages/          # Pages de l'application
│   │   ├── lib/            # Utilitaires et API
│   │   ├── types/          # Définitions TypeScript
│   │   └── hooks/          # Hooks React personnalisés
│   ├── public/             # Assets statiques
│   └── package.json        # Dépendances Node.js
├── backend/                 # API Django
│   ├── vigileos/           # Configuration Django principale
│   ├── users/              # Gestion des utilisateurs
│   ├── sites/              # Gestion des sites
│   ├── equipment/          # Gestion des équipements
│   ├── alerts/             # Gestion des alertes
│   └── requirements.txt    # Dépendances Python
└── docker-compose.yml      # Configuration Docker
```

## Modèles de données

### 1. Sites
```typescript
interface Site {
  id: string;
  name: string;
  address: string;
  city?: string;
  postal_code?: string;
  status: 'online' | 'offline' | 'warning' | 'pending';
  created_at: string;
  updated_at: string;
}
```

### 2. Équipements
```typescript
interface Equipment {
  id: string;
  site_id: string;
  name: string;
  type: 'camera' | 'video-recorder' | 'switch' | 'server' | 'access_point' | 'router' | 'other';
  status: 'online' | 'offline' | 'maintenance';
  ip_address: string | null;
  last_maintenance: string | null;
  created_at: string;
  updated_at: string;
}
```

### 3. Alertes
```typescript
interface Alert {
  id: string;
  equipment_id: string;
  type: 'error' | 'warning' | 'info';
  title: string;
  message: string;
  description?: string;
  status: 'active' | 'resolved' | 'acknowledged';
  created_at: string;
  resolved_at: string | null;
  updated_at?: string;
}
```

### 4. Métriques système
```typescript
interface SystemMetrics {
  cpu_usage: number;
  memory_total: number;
  memory_used: number;
  disk_total: number;
  disk_used: number;
  network_in: number;
  network_out: number;
  timestamp: string;
}
```

## Frontend - Détails techniques

### Dépendances principales
- **React 18.3.1**: Framework principal
- **TypeScript**: Typage statique
- **Vite**: Build tool et dev server
- **Tailwind CSS**: Framework CSS utilitaire
- **shadcn/ui**: Composants UI basés sur Radix UI
- **React Router DOM**: Routage côté client
- **React Hook Form**: Gestion des formulaires
- **Zod**: Validation de schémas
- **Leaflet/MapLibre**: Cartes interactives
- **Recharts**: Graphiques et visualisations
- **Lucide React**: Icônes
- **Tanstack Query**: Gestion d'état et cache API

### Pages principales
1. **Landing** (`/`): Page d'accueil
2. **Index** (`/dashboard`): Tableau de bord principal
3. **Sites** (`/sites`): Gestion des sites
4. **Equipment** (`/equipment`): Gestion des équipements
5. **Alerts** (`/alerts`): Gestion des alertes
6. **Settings** (`/settings`): Paramètres
7. **Account** (`/account`): Gestion du compte

### Composants clés
- **Layout**: Structure principale avec sidebar
- **Sidebar**: Navigation latérale
- **SitesMap**: Carte interactive des sites
- **AuthProvider**: Gestion de l'authentification
- **Equipment components**: Composants spécialisés pour les équipements

## Backend - État actuel

### Applications Django
1. **users**: Gestion des utilisateurs et authentification
2. **sites**: CRUD des sites
3. **equipment**: CRUD des équipements
4. **alerts**: CRUD des alertes

### Configuration actuelle
- **Base de données**: PostgreSQL configurée
- **Authentification**: JWT avec django-rest-framework-simplejwt
- **CORS**: Configuré pour le frontend
- **Modèle utilisateur**: Personnalisé (AUTH_USER_MODEL = 'users.User')

### Dépendances backend
```
Django==4.2.10
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
psycopg2-binary==2.9.9
django-cors-headers==4.3.1
Pillow==10.2.0
```

## API REST - Spécifications

### Base URL
```
http://localhost:8000/api/
```

### Endpoints principaux

#### Sites
- `GET /api/sites/` - Liste des sites
- `GET /api/sites/{id}/` - Détail d'un site
- `POST /api/sites/` - Créer un site
- `PUT /api/sites/{id}/` - Modifier un site
- `DELETE /api/sites/{id}/` - Supprimer un site

#### Équipements
- `GET /api/equipment/` - Liste des équipements
- `GET /api/equipment/{id}/` - Détail d'un équipement
- `GET /api/sites/{site_id}/equipment/` - Équipements d'un site
- `POST /api/equipment/` - Créer un équipement
- `PUT /api/equipment/{id}/` - Modifier un équipement
- `DELETE /api/equipment/{id}/` - Supprimer un équipement

#### Alertes
- `GET /api/alerts/` - Liste des alertes
- `GET /api/alerts/{id}/` - Détail d'une alerte
- `GET /api/equipment/{equipment_id}/alerts/` - Alertes d'un équipement
- `POST /api/alerts/` - Créer une alerte
- `PUT /api/alerts/{id}/` - Modifier une alerte

#### Authentification
- `POST /api/auth/login/` - Connexion (JWT)
- `POST /api/auth/refresh/` - Rafraîchir le token
- `POST /api/auth/register/` - Inscription

## Configuration Docker

### Services
1. **frontend**: Application React (port 8080)
2. **backend**: API Django (port 8000)
3. **vigileos_db**: Base de données PostgreSQL

### Variables d'environnement
```env
# Backend
SECRET_KEY=django-secret-key
DEBUG=1
POSTGRES_DB=vigileos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
ALLOWED_HOSTS=localhost,127.0.0.1,147.93.94.81,vigileospro.com

# Frontend
VITE_API_URL=http://localhost:8000/api
```

## Fonctionnalités métier

### Gestion des sites
- Création, modification, suppression de sites
- Géolocalisation et cartographie
- Statuts: online, offline, warning, pending
- Informations: nom, adresse, ville, code postal

### Gestion des équipements
- Association aux sites
- Types: caméra, enregistreur vidéo, switch, serveur, point d'accès, routeur, autre
- Statuts: online, offline, maintenance
- Adresse IP et maintenance

### Système d'alertes
- Types: error, warning, info
- Statuts: active, resolved, acknowledged
- Association aux équipements
- Horodatage et résolution

### Surveillance et métriques
- Métriques système (CPU, mémoire, disque, réseau)
- Tableaux de bord et visualisations
- Historique des données

## Sécurité

### Authentification
- JWT avec refresh tokens
- Modèle utilisateur personnalisé
- Permissions basées sur les rôles

### CORS
- Configuration pour les domaines autorisés
- Support des credentials

### Validation
- Validation côté frontend (Zod)
- Validation côté backend (Django serializers)

## Développement

### Commandes utiles

#### Frontend
```bash
cd frontend
npm install
npm run dev          # Serveur de développement
npm run build        # Build de production
npm run lint         # Linting
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Docker
```bash
docker-compose up -d     # Lancer tous les services
docker-compose down      # Arrêter tous les services
docker-compose logs      # Voir les logs
```

## Points d'attention pour le développement

### Backend à compléter
1. **Modèles Django**: Créer les modèles pour sites, equipment, alerts
2. **Serializers**: Définir les serializers DRF
3. **ViewSets**: Implémenter les vues API
4. **URLs**: Configurer le routage
5. **Migrations**: Créer et appliquer les migrations
6. **Tests**: Ajouter des tests unitaires et d'intégration

### Fonctionnalités avancées
1. **Pagination**: Implémenter la pagination des listes
2. **Filtrage**: Ajouter des filtres sur les endpoints
3. **Recherche**: Fonctionnalité de recherche
4. **Notifications**: Système de notifications en temps réel
5. **Monitoring**: Métriques et monitoring des équipements
6. **Rapports**: Génération de rapports

### Performance
1. **Cache**: Implémenter du cache (Redis)
2. **Optimisation DB**: Index et optimisations de requêtes
3. **CDN**: Pour les assets statiques
4. **Compression**: Gzip/Brotli

### Déploiement
1. **Production settings**: Configuration pour la production
2. **SSL/TLS**: Certificats HTTPS
3. **Load balancing**: Répartition de charge
4. **Monitoring**: Logs et métriques de production

## Prochaines étapes recommandées

1. **Finaliser les modèles Django** dans chaque app
2. **Créer les serializers DRF** pour l'API
3. **Implémenter les ViewSets** avec CRUD complet
4. **Configurer les URLs** et le routage API
5. **Tester l'intégration** frontend-backend
6. **Ajouter l'authentification JWT** complète
7. **Implémenter les permissions** et la sécurité
8. **Optimiser les performances** et ajouter du cache

Cette base de connaissance devrait vous donner une vue complète du projet Vigileos et vous aider à développer efficacement le backend Django.