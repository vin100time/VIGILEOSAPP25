"""
Health check endpoints for VIGILEOSAPP25
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import time
import redis


def health_check(request):
    """
    Endpoint de vérification de santé complet
    Retourne le statut de tous les services critiques
    """
    start_time = time.time()
    status = {
        'status': 'healthy',
        'timestamp': int(time.time()),
        'services': {},
        'version': '1.0.0',
        'environment': getattr(settings, 'ENVIRONMENT', 'unknown')
    }
    
    # Test de la base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        status['services']['database'] = {
            'status': 'healthy',
            'type': 'postgresql',
            'response_time_ms': round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        status['services']['database'] = {
            'status': 'unhealthy',
            'error': str(e),
            'type': 'postgresql'
        }
        status['status'] = 'unhealthy'
    
    # Test du cache Redis
    cache_start = time.time()
    try:
        # Test simple de lecture/écriture
        test_key = 'health_check_test'
        test_value = 'ok'
        cache.set(test_key, test_value, 10)
        
        if cache.get(test_key) == test_value:
            cache.delete(test_key)
            status['services']['cache'] = {
                'status': 'healthy',
                'type': 'redis',
                'response_time_ms': round((time.time() - cache_start) * 1000, 2)
            }
        else:
            status['services']['cache'] = {
                'status': 'unhealthy',
                'error': 'Cache read/write test failed',
                'type': 'redis'
            }
            status['status'] = 'unhealthy'
    except Exception as e:
        status['services']['cache'] = {
            'status': 'unhealthy',
            'error': str(e),
            'type': 'redis'
        }
        status['status'] = 'unhealthy'
    
    # Test de Celery (si configuré)
    try:
        from celery import current_app
        
        # Vérifier si Celery est configuré
        if hasattr(settings, 'CELERY_BROKER_URL'):
            # Test simple de connexion au broker
            celery_start = time.time()
            inspect = current_app.control.inspect()
            
            # Timeout court pour éviter de bloquer
            active_queues = inspect.active_queues()
            
            if active_queues is not None:
                status['services']['celery'] = {
                    'status': 'healthy',
                    'type': 'task_queue',
                    'workers': len(active_queues) if active_queues else 0,
                    'response_time_ms': round((time.time() - celery_start) * 1000, 2)
                }
            else:
                status['services']['celery'] = {
                    'status': 'unhealthy',
                    'error': 'No active workers found',
                    'type': 'task_queue'
                }
                # Ne pas marquer comme unhealthy si Celery n'est pas critique
    except Exception as e:
        status['services']['celery'] = {
            'status': 'unknown',
            'error': str(e),
            'type': 'task_queue'
        }
    
    # Statistiques générales
    status['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
    
    # Code de statut HTTP basé sur la santé
    http_status = 200 if status['status'] == 'healthy' else 503
    
    return JsonResponse(status, status=http_status)


def simple_health_check(request):
    """
    Endpoint de santé simple pour les load balancers
    Retourne juste un statut OK/KO rapide
    """
    try:
        # Test rapide de la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({'status': 'ok'}, status=200)
    except Exception:
        return JsonResponse({'status': 'error'}, status=503)


def readiness_check(request):
    """
    Endpoint de vérification de disponibilité
    Vérifie si l'application est prête à recevoir du trafic
    """
    checks = []
    
    # Vérifier la base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations")
            migration_count = cursor.fetchone()[0]
        
        checks.append({
            'name': 'database_migrations',
            'status': 'ready' if migration_count > 0 else 'not_ready',
            'details': f'{migration_count} migrations applied'
        })
    except Exception as e:
        checks.append({
            'name': 'database_migrations',
            'status': 'not_ready',
            'error': str(e)
        })
    
    # Vérifier le cache
    try:
        cache.set('readiness_test', 'ok', 5)
        cache_status = 'ready' if cache.get('readiness_test') == 'ok' else 'not_ready'
        cache.delete('readiness_test')
        
        checks.append({
            'name': 'cache',
            'status': cache_status
        })
    except Exception as e:
        checks.append({
            'name': 'cache',
            'status': 'not_ready',
            'error': str(e)
        })
    
    # Déterminer le statut global
    all_ready = all(check['status'] == 'ready' for check in checks)
    
    response = {
        'status': 'ready' if all_ready else 'not_ready',
        'checks': checks
    }
    
    http_status = 200 if all_ready else 503
    return JsonResponse(response, status=http_status)


def liveness_check(request):
    """
    Endpoint de vérification de vie
    Vérifie si l'application est vivante (pas bloquée)
    """
    # Test très simple - si on arrive ici, l'application répond
    return JsonResponse({
        'status': 'alive',
        'timestamp': int(time.time())
    }, status=200)