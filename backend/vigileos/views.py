from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from users.models import User, Company
from sites.models import Site
from equipment.models import Equipment
from alerts.models import Alert
from metrics.models import NetworkMetric


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """Vue dashboard avec statistiques globales."""
    user = request.user
    
    # Filtrer selon les permissions
    if user.is_staff:
        # Admin voit tout
        companies = Company.objects.all()
        sites = Site.objects.all()
        equipment = Equipment.objects.all()
        alerts = Alert.objects.all()
    elif user.company:
        # Utilisateur voit seulement son entreprise
        companies = Company.objects.filter(id=user.company.id)
        sites = Site.objects.filter(company=user.company)
        equipment = Equipment.objects.filter(site__company=user.company)
        alerts = Alert.objects.filter(equipment__site__company=user.company)
    else:
        # Aucune permission
        companies = Company.objects.none()
        sites = Site.objects.none()
        equipment = Equipment.objects.none()
        alerts = Alert.objects.none()
    
    # Statistiques générales
    total_companies = companies.count()
    total_sites = sites.count()
    total_equipment = equipment.count()
    total_users = User.objects.filter(company__in=companies).count() if user.is_staff else User.objects.filter(company=user.company).count()
    
    # Statistiques des équipements
    equipment_by_status = dict(
        equipment.values('status')
        .annotate(count=Count('id'))
        .values_list('status', 'count')
    )
    
    equipment_by_type = dict(
        equipment.values('type')
        .annotate(count=Count('id'))
        .values_list('type', 'count')
    )
    
    # Statistiques des alertes
    total_alerts = alerts.count()
    active_alerts = alerts.filter(status='active').count()
    critical_alerts = alerts.filter(type='error', status__in=['active', 'acknowledged']).count()
    
    alerts_by_type = dict(
        alerts.values('type')
        .annotate(count=Count('id'))
        .values_list('type', 'count')
    )
    
    # Statistiques des sites
    sites_by_status = dict(
        sites.values('status')
        .annotate(count=Count('id'))
        .values_list('status', 'count')
    )
    
    # Métriques récentes (dernières 24h)
    from django.utils import timezone
    from datetime import timedelta
    
    recent_metrics = NetworkMetric.objects.filter(
        equipment__in=equipment,
        timestamp__gte=timezone.now() - timedelta(hours=24)
    )
    
    # Équipements offline
    offline_equipment = equipment.filter(status='offline').count()
    
    # Équipements nécessitant une maintenance
    one_year_ago = timezone.now().date() - timedelta(days=365)
    maintenance_needed = equipment.filter(
        Q(last_maintenance__lt=one_year_ago) | Q(last_maintenance__isnull=True)
    ).count()
    
    dashboard_data = {
        'overview': {
            'total_companies': total_companies,
            'total_sites': total_sites,
            'total_equipment': total_equipment,
            'total_users': total_users,
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'critical_alerts': critical_alerts,
            'offline_equipment': offline_equipment,
            'maintenance_needed': maintenance_needed,
        },
        'equipment': {
            'by_status': equipment_by_status,
            'by_type': equipment_by_type,
        },
        'alerts': {
            'by_type': alerts_by_type,
        },
        'sites': {
            'by_status': sites_by_status,
        },
        'metrics': {
            'recent_count': recent_metrics.count(),
        }
    }
    
    return Response(dashboard_data)