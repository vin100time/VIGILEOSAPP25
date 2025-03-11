#!/bin/sh

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
sleep 10

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

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
"

# Démarrer le serveur
echo "Démarrage du serveur..."
python manage.py runserver 0.0.0.0:8000 