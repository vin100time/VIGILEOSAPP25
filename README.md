# Vigileos - Application de surveillance réseau

## Description
Vigileos est une application web de surveillance d'équipements et de sites. Elle permet de gérer des sites, des équipements et des alertes pour différentes entreprises.

## Prérequis
- Docker
- Docker Compose

## Installation et démarrage

### Méthode 1 : Lancement rapide avec Docker Compose (recommandé)

1. Cloner le dépôt :
```bash
git clone <url-du-dépôt> vigileosapp
cd vigileosapp
```

2. Lancer l'application :
```bash
docker-compose up -d
```

3. Accéder à l'application :
- Frontend : http://localhost:8080
- Backend API : http://localhost:8000
- Interface d'administration Django : http://localhost:8000/admin

### Méthode 2 : Installation manuelle

#### Backend
1. Se déplacer dans le dossier backend :
```bash
cd backend
```

2. Créer un environnement virtuel et installer les dépendances :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer le fichier .env avec vos configurations
```

4. Lancer les migrations :
```bash
python manage.py migrate
```

5. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement :
```bash
python manage.py runserver
```

#### Frontend
1. Se déplacer dans le dossier frontend :
```bash
cd frontend
```

2. Installer les dépendances :
```bash
npm install
```

3. Lancer le serveur de développement :
```bash
npm run dev
```

## Structure du projet
```
vigileosapp/
├── backend/             # Code source du backend Django
│   ├── vigileos/        # Configuration principale Django
│   ├── users/           # Application de gestion des utilisateurs
│   ├── sites/           # Application de gestion des sites
│   ├── equipment/       # Application de gestion des équipements
│   ├── alerts/          # Application de gestion des alertes
│   └── Dockerfile       # Configuration Docker pour le backend
├── frontend/            # Code source du frontend React
│   ├── src/             # Code source React
│   ├── public/          # Fichiers statiques
│   └── Dockerfile       # Configuration Docker pour le frontend
└── docker-compose.yml   # Configuration Docker Compose
```

## Arrêt de l'application
Pour arrêter l'application lancée avec Docker Compose :
```bash
docker-compose down
```

Pour arrêter l'application et supprimer les volumes (données de la base de données) :
```bash
docker-compose down -v
```

## Développement
- Le backend est accessible sur http://localhost:8000
- Le frontend est accessible sur http://localhost:8080
- L'API est documentée dans le fichier `frontend/API_DOCUMENTATION.md`

## Support
Pour toute question ou problème, veuillez créer une issue dans le dépôt GitHub du projet. 