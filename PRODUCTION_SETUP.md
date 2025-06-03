# 🚀 VIGILEOSAPP25 - Configuration Production avec PostgreSQL et Docker

## 📋 Vue d'ensemble

Ce guide détaille la mise en place d'une infrastructure de production scalable pour VIGILEOSAPP25 avec :
- **PostgreSQL** comme base de données principale
- **Redis** pour le cache et les sessions
- **Docker** pour la containerisation
- **Docker Compose** pour l'orchestration multi-services
- **Nginx** comme reverse proxy
- **Configuration multi-environnements** (dev, staging, prod)

## 🏗️ Architecture de Production

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │     Nginx       │    │   Frontend      │
│   (Nginx/HAProxy│────│  Reverse Proxy  │────│   (React)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Django API    │
                       │   (Multiple     │
                       │   Instances)    │
                       └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ PostgreSQL  │ │    Redis    │ │   Celery    │
        │ (Primary)   │ │   (Cache)   │ │  (Tasks)    │
        └─────────────┘ └─────────────┘ └─────────────┘
```

## 🐘 Configuration PostgreSQL

### 1. Installation PostgreSQL

#### Sur Ubuntu/Debian :
```bash
# Installation PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Démarrage du service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Avec Docker :
```bash
# Lancement rapide pour tests
docker run --name vigileosapp-postgres \
  -e POSTGRES_DB=vigileosapp \
  -e POSTGRES_USER=vigileosapp_user \
  -e POSTGRES_PASSWORD=secure_password_123 \
  -p 5432:5432 \
  -d postgres:15
```

### 2. Configuration de la Base de Données

```sql
-- Connexion en tant que superuser
sudo -u postgres psql

-- Création de la base de données
CREATE DATABASE vigileosapp;

-- Création de l'utilisateur
CREATE USER vigileosapp_user WITH PASSWORD 'secure_password_123';

-- Attribution des privilèges
GRANT ALL PRIVILEGES ON DATABASE vigileosapp TO vigileosapp_user;

-- Configuration pour Django
ALTER USER vigileosapp_user CREATEDB;

-- Extensions utiles
\c vigileosapp
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Pour la recherche full-text
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- Pour les index optimisés

-- Quitter
\q
```

### 3. Optimisation PostgreSQL pour Time-Series

```sql
-- Configuration pour les métriques time-series
-- Partitioning par date pour les performances

-- Table partitionnée pour les métriques
CREATE TABLE metrics_networkmetric_partitioned (
    LIKE metrics_networkmetric INCLUDING ALL
) PARTITION BY RANGE (timestamp);

-- Partitions mensuelles (exemple)
CREATE TABLE metrics_networkmetric_2025_01 PARTITION OF metrics_networkmetric_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE metrics_networkmetric_2025_02 PARTITION OF metrics_networkmetric_partitioned
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Index optimisés pour les time-series
CREATE INDEX CONCURRENTLY idx_metrics_timestamp_equipment 
    ON metrics_networkmetric (timestamp DESC, equipment_id);

CREATE INDEX CONCURRENTLY idx_metrics_equipment_timestamp 
    ON metrics_networkmetric (equipment_id, timestamp DESC);
```

## 🐳 Configuration Docker

### 1. Dockerfile pour Django

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=vigileos.settings.production

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copie du code
COPY . .

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Script d'entrée
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "vigileos.wsgi:application"]
```

### 2. Docker Compose pour l'Orchestration

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Base de données PostgreSQL
  postgres:
    image: postgres:15
    container_name: vigileosapp-postgres
    environment:
      POSTGRES_DB: vigileosapp
      POSTGRES_USER: vigileosapp_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - vigileosapp-network
    restart: unless-stopped

  # Cache Redis
  redis:
    image: redis:7-alpine
    container_name: vigileosapp-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - vigileosapp-network
    restart: unless-stopped

  # Application Django
  web:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: vigileosapp-web
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://vigileosapp_user:${POSTGRES_PASSWORD}@postgres:5432/vigileosapp
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - vigileosapp-network
    restart: unless-stopped

  # Worker Celery pour les tâches asynchrones
  celery:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: vigileosapp-celery
    command: celery -A vigileos worker -l info
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://vigileosapp_user:${POSTGRES_PASSWORD}@postgres:5432/vigileosapp
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    volumes:
      - media_volume:/app/media
    depends_on:
      - postgres
      - redis
    networks:
      - vigileosapp-network
    restart: unless-stopped

  # Scheduler Celery Beat
  celery-beat:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: vigileosapp-celery-beat
    command: celery -A vigileos beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://vigileosapp_user:${POSTGRES_PASSWORD}@postgres:5432/vigileosapp
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    volumes:
      - media_volume:/app/media
    depends_on:
      - postgres
      - redis
    networks:
      - vigileosapp-network
    restart: unless-stopped

  # Reverse Proxy Nginx
  nginx:
    image: nginx:alpine
    container_name: vigileosapp-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/sites-available:/etc/nginx/sites-available
      - static_volume:/var/www/static
      - media_volume:/var/www/media
      - ./docker/ssl:/etc/nginx/ssl
    depends_on:
      - web
    networks:
      - vigileosapp-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  vigileosapp-network:
    driver: bridge
```

### 3. Configuration Multi-Environnements

```python
# backend/vigileos/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configuration commune à tous les environnements
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_spectacular',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    
    # Local apps
    'users',
    'sites',
    'equipment',
    'alerts',
    'metrics',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vigileos.urls'

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

```python
# backend/vigileos/settings/production.py
from .base import *
import dj_database_url

DEBUG = False

# Sécurité
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Base de données PostgreSQL
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Configuration PostgreSQL optimisée
DATABASES['default'].update({
    'CONN_MAX_AGE': 60,
    'OPTIONS': {
        'MAX_CONNS': 20,
        'connect_timeout': 10,
    }
})

# Cache Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    }
}

# Sessions dans Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Celery Configuration
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Sécurité HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

## 🔧 Scripts de Déploiement

### 1. Script d'Entrée Docker

```bash
#!/bin/bash
# docker/entrypoint.sh

set -e

# Attendre que PostgreSQL soit prêt
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Migrations de base de données
echo "Running database migrations..."
python manage.py migrate

# Création du superuser si nécessaire
echo "Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vigileosapp.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

# Collecte des fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Chargement des données de test en développement
if [ "$DJANGO_SETTINGS_MODULE" = "vigileos.settings.development" ]; then
    echo "Loading test data..."
    python manage.py shell << EOF
exec(open('load_test_data.py').read())
EOF
fi

echo "Starting application..."
exec "$@"
```

### 2. Configuration Nginx

```nginx
# docker/nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name vigileosapp.com www.vigileosapp.com;
        
        # Redirection HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name vigileosapp.com www.vigileosapp.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Sécurité
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Fichiers statiques
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        location /media/ {
            alias /var/www/media/;
            expires 7d;
        }

        # API Django
        location /api/ {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Admin Django
        location /admin/ {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend React (si servi par Nginx)
        location / {
            root /var/www/frontend;
            try_files $uri $uri/ /index.html;
        }
    }
}
```

## 🚀 Déploiement et Scalabilité

### 1. Variables d'Environnement

```bash
# .env.production
SECRET_KEY=your-super-secret-key-here
POSTGRES_PASSWORD=secure_postgres_password_123
REDIS_PASSWORD=secure_redis_password_123
ALLOWED_HOSTS=vigileosapp.com,www.vigileosapp.com,api.vigileosapp.com
DATABASE_URL=postgresql://vigileosapp_user:secure_postgres_password_123@postgres:5432/vigileosapp
REDIS_URL=redis://:secure_redis_password_123@redis:6379/0
```

### 2. Commandes de Déploiement

```bash
# Déploiement initial
docker-compose -f docker-compose.yml --env-file .env.production up -d

# Mise à jour de l'application
docker-compose -f docker-compose.yml --env-file .env.production pull
docker-compose -f docker-compose.yml --env-file .env.production up -d --no-deps web

# Scaling horizontal
docker-compose -f docker-compose.yml --env-file .env.production up -d --scale web=3 --scale celery=2

# Sauvegarde de la base de données
docker exec vigileosapp-postgres pg_dump -U vigileosapp_user vigileosapp > backup_$(date +%Y%m%d_%H%M%S).sql

# Monitoring des logs
docker-compose logs -f web
docker-compose logs -f celery
```

### 3. Monitoring et Observabilité

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  # Prometheus pour les métriques
  prometheus:
    image: prom/prometheus
    container_name: vigileosapp-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - vigileosapp-network

  # Grafana pour les dashboards
  grafana:
    image: grafana/grafana
    container_name: vigileosapp-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - vigileosapp-network

volumes:
  grafana_data:
```

## 📊 Optimisations de Performance

### 1. Configuration PostgreSQL Avancée

```sql
-- postgresql.conf optimisations
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

### 2. Index Optimisés pour Time-Series

```sql
-- Index pour les requêtes de métriques fréquentes
CREATE INDEX CONCURRENTLY idx_metrics_equipment_time_desc 
    ON metrics_networkmetric (equipment_id, timestamp DESC);

CREATE INDEX CONCURRENTLY idx_metrics_time_range 
    ON metrics_networkmetric USING BRIN (timestamp);

-- Index pour les alertes
CREATE INDEX CONCURRENTLY idx_alerts_status_created 
    ON alerts_alert (status, created_at DESC);

-- Index pour la recherche full-text
CREATE INDEX CONCURRENTLY idx_alerts_search 
    ON alerts_alert USING GIN (to_tsvector('french', title || ' ' || message));
```

## 🔒 Sécurité et Sauvegarde

### 1. Sauvegarde Automatisée

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Sauvegarde PostgreSQL
docker exec vigileosapp-postgres pg_dump -U vigileosapp_user vigileosapp | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Sauvegarde Redis
docker exec vigileosapp-redis redis-cli --rdb /data/dump_$DATE.rdb

# Sauvegarde des fichiers media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/lib/docker/volumes/vigileosapp_media_volume

# Nettoyage des anciennes sauvegardes (garde 30 jours)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

### 2. Monitoring de Santé

```python
# backend/vigileos/health.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis

def health_check(request):
    """Endpoint de vérification de santé"""
    status = {
        'status': 'healthy',
        'database': 'unknown',
        'cache': 'unknown',
        'services': {}
    }
    
    # Test base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['database'] = 'healthy'
    except Exception as e:
        status['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Test cache Redis
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            status['cache'] = 'healthy'
        else:
            status['cache'] = 'unhealthy'
            status['status'] = 'unhealthy'
    except Exception as e:
        status['cache'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    return JsonResponse(status)
```

---

**Cette configuration fournit une base solide pour un déploiement de production scalable et sécurisé ! 🚀**