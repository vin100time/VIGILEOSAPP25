"""
URLs pour l'API InfluxDB.
"""
from django.urls import path
from . import views

app_name = 'influxdb'

urlpatterns = [
    # Métriques d'équipement
    path('equipment/<int:equipment_id>/metrics/', 
         views.record_equipment_metric, 
         name='record-metric'),
    
    path('equipment/<int:equipment_id>/metrics/get/', 
         views.get_equipment_metrics, 
         name='get-metrics'),
    
    path('equipment/<int:equipment_id>/availability/', 
         views.record_availability_check, 
         name='record-availability'),
    
    path('equipment/<int:equipment_id>/dashboard/', 
         views.get_equipment_dashboard, 
         name='equipment-dashboard'),
    
    path('equipment/<int:equipment_id>/availability-report/', 
         views.generate_availability_report, 
         name='availability-report'),
    
    # Résumé par site
    path('sites/<int:site_id>/equipment-summary/', 
         views.get_site_equipment_summary, 
         name='site-equipment-summary'),
]