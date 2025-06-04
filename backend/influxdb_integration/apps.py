from django.apps import AppConfig


class InfluxdbIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'influxdb_integration'
    
    def ready(self):
        # Importer les signaux pour qu'ils soient enregistrés
        from . import services