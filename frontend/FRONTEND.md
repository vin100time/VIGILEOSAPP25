
# Documentation Frontend - Vigileos

## Introduction
Vigileos est une application web de surveillance réseau permettant de gérer et monitorer des sites clients et leurs équipements.

## Architecture Technique

### Frontend
- React 18.3
- TypeScript
- Vite
- TailwindCSS
- Shadcn/UI pour les composants
- React Query pour la gestion des états et des requêtes API
- React Router pour la navigation

## Structure des dossiers
```
src/
├── components/         # Composants réutilisables
│   ├── ui/            # Composants UI génériques (shadcn/ui)
│   ├── equipment/     # Composants liés aux équipements
│   └── Layout.tsx     # Layout principal de l'application
├── hooks/             # Hooks React personnalisés
├── lib/              
│   └── api/           # Clients API pour les différentes ressources
├── pages/             # Pages de l'application
└── types/             # Définitions TypeScript
```

## API Requise

### Sites
- `GET /api/sites` : Liste des sites
- `GET /api/sites/:id` : Détails d'un site
- `POST /api/sites` : Création d'un site
- `PUT /api/sites/:id` : Mise à jour d'un site
- `DELETE /api/sites/:id` : Suppression d'un site

### Équipements
- `GET /api/equipment` : Liste des équipements
- `GET /api/sites/:siteId/equipment` : Équipements d'un site
- `POST /api/equipment` : Création d'un équipement
- `PUT /api/equipment/:id` : Mise à jour d'un équipement
- `DELETE /api/equipment/:id` : Suppression d'un équipement
- `GET /api/equipment/:id` : Détails d'un équipement

### Alertes
- `GET /api/alerts` : Liste des alertes
- `GET /api/equipment/:equipmentId/alerts` : Alertes d'un équipement
- `POST /api/alerts` : Création d'une alerte
- `PUT /api/alerts/:id` : Mise à jour d'une alerte

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
  updated_at?: string;
}
```

## Pages principales

### Dashboard (`/dashboard`)
- Vue d'ensemble des sites et équipements
- Statistiques globales
- Liste des dernières alertes

### Sites (`/sites`)
- Liste des sites clients
- CRUD des sites
- Statut en temps réel

### Équipements
- Liste globale (`/equipements`)
- Par site (`/sites/:siteId/equipment`)
- Détail équipement (`/equipements/:id`)

### Alertes (`/alertes`)
- Liste des alertes actives
- Historique
- Gestion des alertes

## Composants principaux

### Layout
- Sidebar avec navigation
- Header avec actions globales
- Responsive design

### Composants Équipement
- `EquipmentTable` : Tableau des équipements
- `EquipmentFilters` : Filtres de recherche
- `EquipmentIcon` : Icônes par type
- `StatusBadge` : Badge de statut
- `AddEquipmentDialog` : Modal d'ajout
- `EditEquipmentForm` : Formulaire d'édition

## Utilisation de l'API

### Exemple avec React Query
```typescript
// Récupération des sites
const { data: sites, isLoading } = useQuery({
  queryKey: ['sites'],
  queryFn: getSites
});

// Création d'un équipement
const mutation = useMutation({
  mutationFn: createEquipment,
  onSuccess: () => {
    queryClient.invalidateQueries(['equipment']);
    toast({ title: "Équipement créé" });
  }
});
```

### Structure des clients API

Chaque ressource (sites, équipements, alertes) a sa propre classe API :

```typescript
// Exemple pour les sites
export class SitesApi extends ApiClient {
  async getSites(): Promise<Site[]> {
    return this.fetch<Site[]>("/sites");
  }
  
  async createSite(site: Omit<Site, "id" | "created_at" | "updated_at">): Promise<Site> {
    return this.fetch<Site>("/sites", {
      method: "POST",
      body: JSON.stringify(site),
    });
  }
  // ... autres méthodes
}
```

## Gestion des états

### React Query
- Mise en cache automatique
- Revalidation à la demande
- Gestion des erreurs
- Mutations optimistes

### Toast Notifications
Utilisation du composant Toast pour les retours utilisateur :
```typescript
toast({
  title: "Succès",
  description: "L'opération a réussi",
  variant: "success"
});
```

## UI et Styles

### Composants Shadcn/UI
- Button, Card, Dialog
- DataTable
- Form, Input
- Toast

### TailwindCSS
- Classes utilitaires
- Responsive design
- Thème personnalisé
- Support du dark mode

## Bonnes pratiques

### TypeScript
- Types stricts pour toutes les données
- Interfaces pour les modèles
- Types pour les props des composants

### React
- Composants fonctionnels
- Hooks personnalisés
- Gestion d'état avec React Query
- Props typées

### Performance
- Mise en cache des requêtes
- Lazy loading des routes
- Optimisation des re-renders
- Debounce sur les recherches

## Développement

### Installation
```bash
npm install
```

### Variables d'environnement
```bash
VITE_API_URL=http://localhost:3000/api
```

### Développement local
```bash
npm run dev
```

### Build
```bash
npm run build
```

## Tests
Les tests peuvent être ajoutés avec :
- Jest pour les tests unitaires
- React Testing Library pour les tests de composants
- Cypress pour les tests E2E

