
# Documentation API - Vigileos

## Architecture générale

L'application utilise une architecture REST API avec les points d'entrée suivants :

### Base URL
```
http://localhost:3000/api
```

## Points d'entrée API

### 1. Sites

#### GET /sites
Récupère la liste des sites.
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

#### GET /sites/:id
Récupère les détails d'un site spécifique.

#### POST /sites
Crée un nouveau site.
```typescript
// Corps de la requête
{
  name: string;
  address: string;
  city?: string;
  postal_code?: string;
  status: 'online' | 'offline' | 'warning' | 'pending';
}
```

#### PUT /sites/:id
Met à jour un site existant.

#### DELETE /sites/:id
Supprime un site.

### 2. Équipements

#### GET /equipment
Récupère tous les équipements.
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

#### GET /sites/:siteId/equipment
Récupère les équipements d'un site spécifique.

#### POST /equipment
Ajoute un nouvel équipement.

#### PUT /equipment/:id
Met à jour un équipement.

#### DELETE /equipment/:id
Supprime un équipement.

### 3. Alertes

#### GET /alerts
Récupère toutes les alertes.
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

#### GET /equipment/:equipmentId/alerts
Récupère les alertes d'un équipement spécifique.

#### POST /alerts
Crée une nouvelle alerte.

#### PUT /alerts/:id
Met à jour une alerte.

## Gestion des erreurs

Les réponses d'erreur doivent suivre ce format :
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Description détaillée de l'erreur"
  }
}
```

Codes d'erreur HTTP à utiliser :
- 400 : Requête invalide
- 401 : Non authentifié
- 403 : Non autorisé
- 404 : Ressource non trouvée
- 500 : Erreur serveur

## Authentification

L'API utilise une authentification par JWT.

Headers requis :
```
Authorization: Bearer <token>
```

## Réponses API

Format de réponse success :
```json
{
  "data": {
    // données demandées
  },
  "message": "Message de succès"
}
```

## Points d'attention pour l'implémentation

1. Validation des données
   - Valider tous les champs requis
   - Vérifier les formats (emails, dates, etc.)
   - Valider les types d'équipements et statuts

2. Sécurité
   - Implémenter rate limiting
   - Valider les tokens JWT
   - Filtrer les données par utilisateur/organisation

3. Performance
   - Paginer les résultats des listes
   - Mettre en cache les données statiques
   - Optimiser les requêtes de base de données

4. Logging
   - Logger toutes les actions importantes
   - Tracer les erreurs
   - Monitorer les performances

## Tests nécessaires

1. Tests unitaires
   - Validation des données
   - Logique métier
   - Gestion des erreurs

2. Tests d'intégration
   - Flux complets (création site → équipements → alertes)
   - Authentification
   - Permissions

3. Tests de charge
   - Comportement avec beaucoup de données
   - Temps de réponse
   - Limites du système

## Configuration Base de données

Tables requises :
- sites
- equipment
- alerts
- users
- organizations

Les schémas exacts sont définis dans les interfaces TypeScript ci-dessus.

## Environnement de développement

Variables d'environnement requises :
```
DATABASE_URL=
JWT_SECRET=
API_PORT=3000
NODE_ENV=development
```

## Stack technique recommandée

- Node.js avec Express ou NestJS
- PostgreSQL ou MySQL
- Redis pour le caching
- JWT pour l'authentification
- Winston pour le logging

## Installation et démarrage

1. Cloner le repository
```bash
git clone <repository-url>
cd vigileos-api
```

2. Installer les dépendances
```bash
npm install
```

3. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

4. Lancer les migrations de base de données
```bash
npm run migrate
```

5. Démarrer le serveur
```bash
npm run dev  # Pour le développement
npm start    # Pour la production
```

## Support et contact

Pour toute question ou problème concernant l'API, contacter :
- Email : support@vigileos.com
- Téléphone : +33 1 23 45 67 89

---
Documentation générée le [Date actuelle]
Version 1.0.0
