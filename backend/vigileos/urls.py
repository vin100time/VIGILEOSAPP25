from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .health import health_check, simple_health_check, readiness_check, liveness_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('sites.urls')),
    path('api/', include('equipment.urls')),
    path('api/', include('alerts.urls')),
    path('api/', include('metrics.urls')),
    
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
