
# Documentation Vigileos

## Vue d'ensemble
Vigileos est une application web de surveillance réseau permettant de gérer et monitorer des sites clients et leurs équipements.

## Architecture Technique

### Frontend
- React 18.3 avec TypeScript
- Vite pour le build
- TailwindCSS pour le styling
- Shadcn/UI pour les composants
- React Query pour la gestion des états
- React Router pour la navigation

### API REST
Base URL: `http://localhost:3000/api`

#### Endpoints Sites
- `GET /sites` : Liste des sites
- `GET /sites/:id` : Détails d'un site
- `POST /sites` : Création d'un site
- `PUT /sites/:id` : Mise à jour d'un site
- `DELETE /sites/:id` : Suppression d'un site

#### Endpoints Équipements
- `GET /equipment` : Liste des équipements
- `GET /sites/:siteId/equipment` : Équipements d'un site
- `POST /equipment` : Création d'un équipement
- `PUT /equipment/:id` : Mise à jour d'un équipement
- `DELETE /equipment/:id` : Suppression d'un équipement

#### Endpoints Alertes
- `GET /alerts` : Liste des alertes
- `GET /equipment/:equipmentId/alerts` : Alertes d'un équipement
- `POST /alerts` : Création d'une alerte
- `PUT /alerts/:id` : Mise à jour d'une alerte

## Types de données

### Site
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

### Equipment
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

### Alert
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
}
```

## Authentification
L'application utilise une authentification simple basée sur localStorage pour le développement.

## Installation et Développement

### Prérequis
- Node.js 18+
- npm ou yarn
- Docker (optionnel)

### Installation
```bash
npm install
```

### Développement local
```bash
npm run dev
```

### Build et déploiement
```bash
# Build
npm run build

# Docker
docker-compose up --build
```

## Points d'attention
1. Gestion des erreurs API centralisée
2. Validation des données côté client
3. Gestion du cache avec React Query
4. Responsive design
5. Gestion des états de chargement

## Support
Pour toute question technique, contactez l'équipe de développement.
