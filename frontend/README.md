
# Vigileos - Application de surveillance réseau

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

### API Requise
L'application nécessite une API REST avec les endpoints suivants :

#### Authentification
- `POST /api/auth/login` : Connexion utilisateur
- `POST /api/auth/register` : Inscription utilisateur
- `POST /api/auth/logout` : Déconnexion

#### Sites
- `GET /api/sites` : Liste des sites
- `GET /api/sites/:id` : Détails d'un site
- `POST /api/sites` : Création d'un site
- `PUT /api/sites/:id` : Mise à jour d'un site
- `DELETE /api/sites/:id` : Suppression d'un site

#### Équipements
- `GET /api/equipment` : Liste des équipements
- `GET /api/sites/:siteId/equipment` : Équipements d'un site
- `POST /api/equipment` : Création d'un équipement
- `PUT /api/equipment/:id` : Mise à jour d'un équipement
- `DELETE /api/equipment/:id` : Suppression d'un équipement
- `GET /api/equipment/:id` : Détails d'un équipement

#### Alertes
- `GET /api/alerts` : Liste des alertes
- `GET /api/equipment/:equipmentId/alerts` : Alertes d'un équipement
- `POST /api/alerts` : Création d'une alerte
- `PUT /api/alerts/:id` : Mise à jour d'une alerte

### Types de données

Les types de données sont définis dans `src/types/database.ts`. Ils incluent :
- `Site` : Informations sur un site client
- `Equipment` : Informations sur un équipement
- `Alert` : Informations sur une alerte
- `SystemMetrics` : Métriques système pour la surveillance

### Authentification
L'application utilise une authentification par token JWT. Le token est stocké dans le localStorage et doit être inclus dans les headers des requêtes API :
```
Authorization: Bearer <token>
```

## Installation et développement

1. Installation des dépendances :
```bash
npm install
```

2. Configuration des variables d'environnement :
```bash
VITE_API_URL=http://localhost:3000/api
```

3. Lancement du serveur de développement :
```bash
npm run dev
```

## Build et déploiement

1. Construction de l'application :
```bash
npm run build
```

2. Les fichiers de production seront générés dans le dossier `dist`.

## Développement backend requis

Pour implémenter le backend, vous devez :

1. Créer une API REST respectant les endpoints listés ci-dessus
2. Implémenter l'authentification JWT
3. Respecter les types de données définis dans `src/types/database.ts`
4. Assurer la validation des données côté serveur
5. Gérer les erreurs de manière appropriée avec des codes HTTP standards

### Format des réponses

Les réponses de l'API doivent suivre ce format :

Succès :
```json
{
  "data": { ... },
  "message": "Success message"
}
```

Erreur :
```json
{
  "error": {
    "message": "Error message",
    "code": "ERROR_CODE"
  }
}
```

## Tests

Pour les tests d'intégration, assurez-vous que :
1. L'API respecte les types TypeScript définis
2. Les réponses suivent le format attendu
3. L'authentification fonctionne correctement
4. Les erreurs sont gérées de manière appropriée

