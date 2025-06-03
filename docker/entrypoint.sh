#!/bin/bash

set -e

echo "🚀 Starting VIGILEOSAPP25 Backend..."

# Function to wait for a service
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    
    echo "⏳ Waiting for $service_name to be ready..."
    while ! nc -z $host $port; do
        sleep 0.5
    done
    echo "✅ $service_name is ready!"
}

# Wait for PostgreSQL
if [ "$DATABASE_URL" ]; then
    # Extract host and port from DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ "$DB_HOST" ] && [ "$DB_PORT" ]; then
        wait_for_service $DB_HOST $DB_PORT "PostgreSQL"
    fi
fi

# Wait for Redis
if [ "$REDIS_URL" ]; then
    # Extract host and port from REDIS_URL
    REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ "$REDIS_HOST" ] && [ "$REDIS_PORT" ]; then
        wait_for_service $REDIS_HOST $REDIS_PORT "Redis"
    fi
fi

echo "📊 Running database migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@vigileosapp.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superuser "{username}" created successfully')
else:
    print(f'ℹ️  Superuser "{username}" already exists')
EOF

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Load initial data in development
if [ "$DJANGO_SETTINGS_MODULE" = "vigileos.settings.development" ]; then
    echo "🔧 Loading development data..."
    python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model
from sites.models import Site
from equipment.models import Equipment
from alerts.models import Alert
from metrics.models import NetworkMetric
from datetime import datetime, timedelta
import random

# Create test sites if they don't exist
if not Site.objects.exists():
    sites_data = [
        {'name': 'Site Principal Paris', 'location': 'Paris, France', 'description': 'Site principal de l\'entreprise'},
        {'name': 'Site Secondaire Lyon', 'location': 'Lyon, France', 'description': 'Site de sauvegarde'},
        {'name': 'Datacenter Marseille', 'location': 'Marseille, France', 'description': 'Centre de données principal'},
    ]
    
    for site_data in sites_data:
        site = Site.objects.create(**site_data)
        print(f'✅ Site créé: {site.name}')
        
        # Create equipment for each site
        equipment_types = ['Router', 'Switch', 'Firewall', 'Server']
        for i, eq_type in enumerate(equipment_types):
            equipment = Equipment.objects.create(
                name=f'{eq_type}-{site.name.split()[0]}-{i+1:02d}',
                equipment_type=eq_type,
                ip_address=f'192.168.{site.id}.{i+10}',
                site=site,
                status='active'
            )
            print(f'✅ Équipement créé: {equipment.name}')
            
            # Create some metrics
            for j in range(10):
                NetworkMetric.objects.create(
                    equipment=equipment,
                    cpu_usage=random.uniform(10, 90),
                    memory_usage=random.uniform(20, 80),
                    bandwidth_usage=random.uniform(5, 95),
                    timestamp=datetime.now() - timedelta(hours=j)
                )
            
            # Create some alerts
            if random.choice([True, False]):
                Alert.objects.create(
                    title=f'Alerte {eq_type} - {site.name}',
                    message=f'Utilisation CPU élevée détectée sur {equipment.name}',
                    severity=random.choice(['low', 'medium', 'high', 'critical']),
                    equipment=equipment,
                    status='active'
                )

print('🎉 Données de test chargées avec succès!')
EOF
fi

echo "🎯 Starting application with command: $@"
exec "$@"