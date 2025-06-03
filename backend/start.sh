#!/bin/bash

# Script de démarrage rapide pour VIGILEOS Backend

echo "🚀 Démarrage de VIGILEOS Backend..."

# Configuration de l'environnement
export DJANGO_SETTINGS_MODULE=vigileos.settings.development
export DEBUG=True

# Vérification des dépendances
echo "📦 Vérification des dépendances..."
python -c "import django, rest_framework, django_filters, rest_framework_simplejwt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dépendances manquantes. Installation..."
    pip install django djangorestframework django-filter djangorestframework-simplejwt django-cors-headers drf-spectacular
fi

# Migration de la base de données
echo "🗄️  Migration de la base de données..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Création des données de test si nécessaire
echo "📊 Vérification des données de test..."
python -c "
from users.models import User
if not User.objects.filter(username='admin').exists():
    print('Création des données de test...')
    exec(open('create_test_data.py').read())
else:
    print('Données de test déjà présentes')
"

# Démarrage du serveur
echo "🌐 Démarrage du serveur sur http://localhost:12000"
echo "📚 Documentation API: http://localhost:12000/api/docs/"
echo "🔐 Connexion test: admin / admin123"
echo ""
echo "Endpoints principaux:"
echo "  - POST /api/auth/login/ - Authentification"
echo "  - GET /api/dashboard/ - Dashboard global"
echo "  - GET /api/users/ - Utilisateurs"
echo "  - GET /api/companies/ - Entreprises"
echo "  - GET /api/sites/ - Sites"
echo "  - GET /api/equipment/ - Équipements"
echo "  - GET /api/alerts/ - Alertes"
echo "  - GET /api/metrics/ - Métriques"
echo ""

# Arrêt des serveurs existants
pkill -f "python manage.py runserver" 2>/dev/null

# Démarrage du serveur
python manage.py runserver 0.0.0.0:12000