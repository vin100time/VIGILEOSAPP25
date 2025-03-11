#!/bin/bash

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
sleep 10

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

# Créer un superutilisateur si nécessaire
echo "Création d'un superutilisateur..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

echo "Initialisation terminée !" 