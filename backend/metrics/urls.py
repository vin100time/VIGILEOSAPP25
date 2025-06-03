from rest_framework.routers import DefaultRouter
from .views import NetworkMetricViewSet, AlertThresholdViewSet

router = DefaultRouter()
router.register(r'metrics', NetworkMetricViewSet, basename='metric')
router.register(r'thresholds', AlertThresholdViewSet, basename='threshold')

urlpatterns = router.urls