from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .health import health_check, simple_health_check, readiness_check, liveness_check
from .views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('sites.urls', namespace='sites')),
    path('api/', include('equipment.urls', namespace='equipment')),
    path('api/', include('alerts.urls', namespace='alerts')),
    path('api/', include('metrics.urls', namespace='metrics')),
    path('api/', include('influxdb_integration.urls', namespace='influxdb')),
    path('api/dashboard/', dashboard_view, name='dashboard'),
    
    # Documentation API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Health checks
    path('api/health/', health_check, name='health-check'),
    path('health/', simple_health_check, name='simple-health-check'),
    path('api/readiness/', readiness_check, name='readiness-check'),
    path('api/liveness/', liveness_check, name='liveness-check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
