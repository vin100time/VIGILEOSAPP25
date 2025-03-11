from django.db import migrations
import datetime
from django.utils import timezone

def create_test_alerts(apps, schema_editor):
    Alert = apps.get_model('alerts', 'Alert')
    Equipment = apps.get_model('equipment', 'Equipment')
    
    # Fonction pour créer des alertes pour un équipement
    def create_alerts_for_equipment(equipment_name, alerts_list):
        try:
            equipment = Equipment.objects.get(name=equipment_name)
            for alert in alerts_list:
                Alert.objects.get_or_create(
                    title=alert['title'],
                    equipment=equipment,
                    defaults={
                        'message': alert['message'],
                        'type': alert['type'],
                        'status': alert['status'],
                        'created_at': alert.get('created_at', timezone.now()),
                        'resolved_at': alert.get('resolved_at')
                    }
                )
        except Equipment.DoesNotExist:
            pass
    
    # Alertes pour la caméra parking de Lyon
    create_alerts_for_equipment("Caméra Parking", [
        {
            'title': 'Perte de signal intermittente',
            'message': 'La caméra présente des pertes de signal intermittentes. Vérifier la connexion réseau.',
            'type': 'warning',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(hours=5)
        }
    ])
    
    # Alertes pour la caméra extérieure de Marseille
    create_alerts_for_equipment("Caméra Extérieure", [
        {
            'title': 'Caméra hors ligne',
            'message': 'La caméra est complètement hors ligne. Vérifier l\'alimentation et la connexion réseau.',
            'type': 'error',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(days=1)
        }
    ])
    
    # Alertes pour le serveur stockage de Marseille
    create_alerts_for_equipment("Serveur Stockage", [
        {
            'title': 'Espace disque faible',
            'message': 'L\'espace disque disponible est inférieur à 10%. Nettoyer les anciens enregistrements.',
            'type': 'warning',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(hours=12)
        },
        {
            'title': 'Température CPU élevée',
            'message': 'La température du CPU a dépassé 75°C. Vérifier la ventilation.',
            'type': 'warning',
            'status': 'acknowledged',
            'created_at': timezone.now() - timezone.timedelta(days=2)
        }
    ])
    
    # Alertes pour les équipements de Bordeaux
    create_alerts_for_equipment("Caméra Entrée", [
        {
            'title': 'Perte de connexion',
            'message': 'La caméra a perdu sa connexion au réseau. Vérifier le switch et les câbles.',
            'type': 'error',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(hours=8)
        }
    ])
    
    create_alerts_for_equipment("Switch Réseau", [
        {
            'title': 'Équipement hors ligne',
            'message': 'Le switch est hors ligne. Vérifier l\'alimentation électrique du local technique.',
            'type': 'error',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(hours=8)
        }
    ])
    
    # Alertes pour le magasin Nice
    create_alerts_for_equipment("Caméra Entrée", [
        {
            'title': 'Qualité d\'image dégradée',
            'message': 'La qualité d\'image est dégradée. Vérifier la mise au point et le nettoyage de l\'objectif.',
            'type': 'warning',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(days=1)
        }
    ])
    
    create_alerts_for_equipment("Serveur Local", [
        {
            'title': 'Erreurs disque détectées',
            'message': 'Des erreurs ont été détectées sur le disque dur. Planifier un remplacement.',
            'type': 'warning',
            'status': 'acknowledged',
            'created_at': timezone.now() - timezone.timedelta(days=3)
        },
        {
            'title': 'Mise à jour disponible',
            'message': 'Une mise à jour de sécurité importante est disponible. Planifier l\'installation.',
            'type': 'info',
            'status': 'active',
            'created_at': timezone.now() - timezone.timedelta(days=5)
        }
    ])
    
    # Alertes résolues (pour l'historique)
    create_alerts_for_equipment("Routeur Internet", [
        {
            'title': 'Redémarrage inattendu',
            'message': 'Le routeur a redémarré de façon inattendue. Surveillance recommandée.',
            'type': 'warning',
            'status': 'resolved',
            'created_at': timezone.now() - timezone.timedelta(days=10),
            'resolved_at': timezone.now() - timezone.timedelta(days=9)
        }
    ])
    
    create_alerts_for_equipment("PC Surveillance", [
        {
            'title': 'Utilisation CPU élevée',
            'message': 'Utilisation CPU anormalement élevée. Vérifier les processus en cours.',
            'type': 'warning',
            'status': 'resolved',
            'created_at': timezone.now() - timezone.timedelta(days=7),
            'resolved_at': timezone.now() - timezone.timedelta(days=6)
        }
    ])

def delete_test_alerts(apps, schema_editor):
    Alert = apps.get_model('alerts', 'Alert')
    Alert.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
        ('equipment', '0002_create_test_equipment'),
    ]

    operations = [
        migrations.RunPython(create_test_alerts, delete_test_alerts),
    ] 