#!/bin/sh

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
sleep 10

# S'assurer que le répertoire des migrations existe pour toutes les applications
echo "Vérification des répertoires de migrations..."
mkdir -p users/migrations
mkdir -p sites/migrations
mkdir -p equipment/migrations
mkdir -p alerts/migrations
touch users/migrations/__init__.py
touch sites/migrations/__init__.py
touch equipment/migrations/__init__.py
touch alerts/migrations/__init__.py

# Supprimer toutes les migrations existantes
echo "Suppression des migrations existantes..."
rm -f users/migrations/0*.py
rm -f sites/migrations/0*.py
rm -f equipment/migrations/0*.py
rm -f alerts/migrations/0*.py

# Effectuer les makemigrations pour toutes les applications
echo "Création des migrations initiales..."
python manage.py makemigrations users --noinput
python manage.py makemigrations sites --noinput
python manage.py makemigrations equipment --noinput
python manage.py makemigrations alerts --noinput

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate auth --noinput
python manage.py migrate admin --noinput
python manage.py migrate contenttypes --noinput
python manage.py migrate sessions --noinput
python manage.py migrate users --noinput
python manage.py migrate sites --noinput
python manage.py migrate equipment --noinput
python manage.py migrate alerts --noinput

# Créer les données de test si nécessaire
echo "Création des données de test..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

# Créer les utilisateurs de test
echo "Création des utilisateurs de test..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from users.models import Company

User = get_user_model()

# Créer les entreprises
try:
    logistique, _ = Company.objects.get_or_create(
        name='Entreprise de Logistique',
        defaults={'address': '15 avenue de la Logistique, 75001 Paris'}
    )

    banque, _ = Company.objects.get_or_create(
        name='Groupe Bancaire',
        defaults={'address': '25 rue de la Finance, 59000 Lille'}
    )

    magasins, _ = Company.objects.get_or_create(
        name='Chaîne de Magasins',
        defaults={'address': '8 boulevard du Commerce, 31000 Toulouse'}
    )

    # Créer les utilisateurs
    if not User.objects.filter(username='paul').exists():
        User.objects.create_user(
            'paul', 'paul@logistique.fr', 'paul123',
            first_name='Paul', last_name='Dupont',
            company=logistique
        )

    if not User.objects.filter(username='sophie').exists():
        User.objects.create_user(
            'sophie', 'sophie@banque.fr', 'sophie123',
            first_name='Sophie', last_name='Martin',
            company=banque
        )

    if not User.objects.filter(username='karim').exists():
        User.objects.create_user(
            'karim', 'karim@magasins.fr', 'karim123',
            first_name='Karim', last_name='Benali',
            company=magasins
        )
except Exception as e:
    print(f'Erreur lors de la création des utilisateurs: {e}')
"

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Démarrer le serveur
echo "Démarrage du serveur..."
python manage.py runserver 0.0.0.0:8000 