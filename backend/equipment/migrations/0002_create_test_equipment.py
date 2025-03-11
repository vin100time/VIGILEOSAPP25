from django.db import migrations
import datetime

def create_test_equipment(apps, schema_editor):
    Equipment = apps.get_model('equipment', 'Equipment')
    Site = apps.get_model('sites', 'Site')
    
    # Fonction pour créer des équipements pour un site
    def create_equipment_for_site(site_name, equipment_list):
        try:
            site = Site.objects.get(name=site_name)
            for eq in equipment_list:
                Equipment.objects.get_or_create(
                    name=eq['name'],
                    site=site,
                    defaults={
                        'type': eq['type'],
                        'status': eq['status'],
                        'ip_address': eq.get('ip_address'),
                        'last_maintenance': eq.get('last_maintenance')
                    }
                )
        except Site.DoesNotExist:
            pass
    
    # Équipements pour l'agence Paris
    create_equipment_for_site("Agence Paris", [
        {'name': 'Caméra Entrée', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.1.10'},
        {'name': 'Caméra Entrepôt', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.1.11'},
        {'name': 'Serveur Principal', 'type': 'server', 'status': 'online', 'ip_address': '192.168.1.2', 'last_maintenance': datetime.date(2023, 12, 15)},
        {'name': 'Switch Réseau', 'type': 'switch', 'status': 'online', 'ip_address': '192.168.1.1', 'last_maintenance': datetime.date(2023, 11, 10)},
        {'name': 'Routeur Internet', 'type': 'router', 'status': 'online', 'ip_address': '192.168.1.254', 'last_maintenance': datetime.date(2023, 10, 5)}
    ])
    
    # Équipements pour l'agence Lyon
    create_equipment_for_site("Agence Lyon", [
        {'name': 'Caméra Accueil', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.2.10'},
        {'name': 'Caméra Parking', 'type': 'camera', 'status': 'warning', 'ip_address': '192.168.2.11'},
        {'name': 'Enregistreur Vidéo', 'type': 'video-recorder', 'status': 'online', 'ip_address': '192.168.2.20', 'last_maintenance': datetime.date(2023, 9, 20)},
        {'name': 'Switch Principal', 'type': 'switch', 'status': 'online', 'ip_address': '192.168.2.1', 'last_maintenance': datetime.date(2023, 8, 15)}
    ])
    
    # Équipements pour l'agence Marseille
    create_equipment_for_site("Agence Marseille", [
        {'name': 'Caméra Extérieure', 'type': 'camera', 'status': 'offline', 'ip_address': '192.168.3.10'},
        {'name': 'Caméra Quai', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.3.11'},
        {'name': 'Serveur Stockage', 'type': 'server', 'status': 'warning', 'ip_address': '192.168.3.2', 'last_maintenance': datetime.date(2023, 7, 10)},
        {'name': 'Point d\'accès WiFi', 'type': 'access_point', 'status': 'online', 'ip_address': '192.168.3.100', 'last_maintenance': datetime.date(2023, 6, 5)}
    ])
    
    # Équipements pour l'agence Lille
    create_equipment_for_site("Agence Lille", [
        {'name': 'Caméra Salle des Coffres', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.4.10'},
        {'name': 'Caméra Guichets', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.4.11'},
        {'name': 'Serveur Sécurisé', 'type': 'server', 'status': 'online', 'ip_address': '192.168.4.2', 'last_maintenance': datetime.date(2023, 12, 1)},
        {'name': 'Routeur Principal', 'type': 'router', 'status': 'online', 'ip_address': '192.168.4.1', 'last_maintenance': datetime.date(2023, 11, 20)}
    ])
    
    # Équipements pour l'agence Bordeaux
    create_equipment_for_site("Agence Bordeaux", [
        {'name': 'Caméra Entrée', 'type': 'camera', 'status': 'offline', 'ip_address': '192.168.5.10'},
        {'name': 'Caméra Distributeur', 'type': 'camera', 'status': 'offline', 'ip_address': '192.168.5.11'},
        {'name': 'Switch Réseau', 'type': 'switch', 'status': 'offline', 'ip_address': '192.168.5.1', 'last_maintenance': datetime.date(2023, 10, 15)}
    ])
    
    # Équipements pour l'agence Nantes
    create_equipment_for_site("Agence Nantes", [
        {'name': 'Caméra Accueil', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.6.10'},
        {'name': 'Caméra Bureaux', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.6.11'},
        {'name': 'Serveur Local', 'type': 'server', 'status': 'online', 'ip_address': '192.168.6.2', 'last_maintenance': datetime.date(2023, 9, 10)},
        {'name': 'PC Surveillance', 'type': 'pc', 'status': 'online', 'ip_address': '192.168.6.100', 'last_maintenance': datetime.date(2023, 8, 5)}
    ])
    
    # Équipements pour le magasin Toulouse
    create_equipment_for_site("Magasin Toulouse", [
        {'name': 'Caméra Entrée', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.7.10'},
        {'name': 'Caméra Rayons', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.7.11'},
        {'name': 'Caméra Caisses', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.7.12'},
        {'name': 'Enregistreur Vidéo', 'type': 'video-recorder', 'status': 'online', 'ip_address': '192.168.7.20', 'last_maintenance': datetime.date(2023, 7, 15)},
        {'name': 'Switch Principal', 'type': 'switch', 'status': 'online', 'ip_address': '192.168.7.1', 'last_maintenance': datetime.date(2023, 6, 10)}
    ])
    
    # Équipements pour le magasin Nice
    create_equipment_for_site("Magasin Nice", [
        {'name': 'Caméra Entrée', 'type': 'camera', 'status': 'warning', 'ip_address': '192.168.8.10'},
        {'name': 'Caméra Réserve', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.8.11'},
        {'name': 'Serveur Local', 'type': 'server', 'status': 'warning', 'ip_address': '192.168.8.2', 'last_maintenance': datetime.date(2023, 5, 20)},
        {'name': 'Point d\'accès WiFi', 'type': 'access_point', 'status': 'online', 'ip_address': '192.168.8.100', 'last_maintenance': datetime.date(2023, 4, 15)}
    ])
    
    # Équipements pour le magasin Strasbourg
    create_equipment_for_site("Magasin Strasbourg", [
        {'name': 'Caméra Entrée', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.9.10'},
        {'name': 'Caméra Parking', 'type': 'camera', 'status': 'online', 'ip_address': '192.168.9.11'},
        {'name': 'Routeur Principal', 'type': 'router', 'status': 'online', 'ip_address': '192.168.9.1', 'last_maintenance': datetime.date(2023, 3, 10)},
        {'name': 'PC Gérant', 'type': 'pc', 'status': 'online', 'ip_address': '192.168.9.100', 'last_maintenance': datetime.date(2023, 2, 5)}
    ])

def delete_test_equipment(apps, schema_editor):
    Equipment = apps.get_model('equipment', 'Equipment')
    Equipment.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
        ('sites', '0002_create_test_sites'),
    ]

    operations = [
        migrations.RunPython(create_test_equipment, delete_test_equipment),
    ] 