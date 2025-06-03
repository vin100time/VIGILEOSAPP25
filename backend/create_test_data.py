#!/usr/bin/env python
"""
Script pour créer des données de test pour VIGILEOSAPP25
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vigileos.settings.development')
django.setup()

from users.models import User, Company
from sites.models import Site
from equipment.models import Equipment
from alerts.models import Alert
from metrics.models import NetworkMetric, AlertThreshold

def create_test_data():
    print("🚀 Création des données de test...")
    
    # 1. Créer des entreprises
    print("📊 Création des entreprises...")
    companies = []
    company_data = [
        {"name": "TechCorp Solutions", "address": "123 Avenue des Technologies, 75001 Paris"},
        {"name": "IndustrieMax", "address": "456 Rue de l'Industrie, 69000 Lyon"},
        {"name": "SecureNet", "address": "789 Boulevard de la Sécurité, 13000 Marseille"},
    ]
    
    for data in company_data:
        company, created = Company.objects.get_or_create(
            name=data["name"],
            defaults={"address": data["address"]}
        )
        companies.append(company)
        if created:
            print(f"  ✅ Entreprise créée: {company.name}")
        else:
            print(f"  ℹ️  Entreprise existante: {company.name}")
    
    # 2. Créer des utilisateurs
    print("👥 Création des utilisateurs...")
    users_data = [
        {"username": "manager1", "email": "manager1@techcorp.com", "first_name": "Jean", "last_name": "Dupont", "company": companies[0], "is_staff": True},
        {"username": "tech1", "email": "tech1@techcorp.com", "first_name": "Marie", "last_name": "Martin", "company": companies[0]},
        {"username": "admin2", "email": "admin@industriemax.com", "first_name": "Pierre", "last_name": "Durand", "company": companies[1], "is_staff": True},
        {"username": "operator1", "email": "operator@securenet.com", "first_name": "Sophie", "last_name": "Bernard", "company": companies[2]},
    ]
    
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data["username"],
            defaults={
                "email": data["email"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "company": data["company"],
                "is_staff": data.get("is_staff", False),
                "phone": f"+33 6 {data['username'][-1]}0 00 00 0{data['username'][-1]}"
            }
        )
        if created:
            user.set_password("password123")
            user.save()
            print(f"  ✅ Utilisateur créé: {user.username} ({user.company.name})")
        else:
            print(f"  ℹ️  Utilisateur existant: {user.username}")
    
    # 3. Créer des sites
    print("🏢 Création des sites...")
    sites_data = [
        {"name": "Site Principal Paris", "address": "123 Avenue des Technologies, 75001 Paris", "company": companies[0]},
        {"name": "Datacenter Nord", "address": "456 Rue du Datacenter, 59000 Lille", "company": companies[0]},
        {"name": "Usine Lyon", "address": "456 Rue de l'Industrie, 69000 Lyon", "company": companies[1]},
        {"name": "Centre de Contrôle", "address": "789 Boulevard de la Sécurité, 13000 Marseille", "company": companies[2]},
        {"name": "Site Secondaire", "address": "321 Rue de la Backup, 13001 Marseille", "company": companies[2]},
    ]
    
    sites = []
    for data in sites_data:
        site, created = Site.objects.get_or_create(
            name=data["name"],
            company=data["company"],
            defaults={"address": data["address"]}
        )
        sites.append(site)
        if created:
            print(f"  ✅ Site créé: {site.name} ({site.company.name})")
        else:
            print(f"  ℹ️  Site existant: {site.name}")
    
    # 4. Créer des équipements
    print("🖥️  Création des équipements...")
    equipment_types = ["Serveur", "Switch", "Routeur", "Firewall", "UPS", "Caméra"]
    statuses = ["active", "maintenance", "inactive"]
    
    equipments = []
    for i, site in enumerate(sites):
        for j in range(3, 8):  # 3 à 7 équipements par site
            equipment_type = equipment_types[j % len(equipment_types)]
            # Mapper les types d'équipements aux choix du modèle
            type_mapping = {
                "Serveur": "server",
                "Switch": "switch", 
                "Routeur": "router",
                "Firewall": "other",
                "UPS": "other",
                "Caméra": "camera"
            }
            
            # Mapper les statuts
            status_mapping = {
                "active": "online",
                "maintenance": "warning", 
                "inactive": "offline"
            }
            
            equipment, created = Equipment.objects.get_or_create(
                name=f"{equipment_type}-{site.name.split()[0]}-{j:02d}",
                site=site,
                defaults={
                    "type": type_mapping.get(equipment_type, "other"),
                    "status": status_mapping.get(statuses[j % len(statuses)], "online"),
                    "ip_address": f"192.168.{i+1}.{j+10}",
                    "last_maintenance": timezone.now().date() - timedelta(days=j*7) if j % 3 == 0 else None,
                }
            )
            equipments.append(equipment)
            if created:
                print(f"  ✅ Équipement créé: {equipment.name} ({equipment.site.name})")
    
    # 5. Créer des seuils d'alerte
    print("⚠️  Création des seuils d'alerte...")
    for i, equipment in enumerate(equipments[:5]):  # Seuils pour les 5 premiers équipements
        threshold, created = AlertThreshold.objects.get_or_create(
            equipment=equipment,
            defaults={
                "cpu_warning_threshold": 70.0 + (i * 5),
                "cpu_critical_threshold": 90.0 + (i * 2),
                "memory_warning_threshold": 80.0,
                "memory_critical_threshold": 95.0,
                "disk_warning_threshold": 85.0,
                "disk_critical_threshold": 95.0,
                "ping_warning_threshold": 100.0,
                "ping_critical_threshold": 500.0,
                "packet_loss_warning": 5.0,
                "packet_loss_critical": 20.0,
            }
        )
        if created:
            print(f"  ✅ Seuils créés pour {threshold.equipment.name}")
    
    # 6. Créer des métriques réseau
    print("📊 Création des métriques réseau...")
    for i, equipment in enumerate(equipments[:10]):  # Métriques pour les 10 premiers équipements
        for days_ago in range(7):  # 7 jours de données
            for hour in range(0, 24, 4):  # Toutes les 4 heures
                timestamp = timezone.now() - timedelta(days=days_ago, hours=hour)
                
                # Générer des valeurs réalistes
                base_cpu = 30 + (i * 5) % 50
                base_ping = 10 + (i * 2) % 30
                base_packet_loss = (i % 5) * 0.5
                
                # Ajouter de la variation
                cpu_usage = base_cpu + (hour % 12) * 2 + (days_ago % 3) * 5
                ping_time = base_ping + (hour % 6) * 5 + (days_ago % 2) * 10
                packet_loss = base_packet_loss + (hour % 4) * 0.2
                
                # Calculer les tailles mémoire et disque
                memory_total = 8 * 1024 * 1024 * 1024  # 8GB
                memory_used = int(memory_total * (40 + (i * 7) % 40 + (hour % 8) * 3) / 100)
                disk_total = 500 * 1024 * 1024 * 1024  # 500GB
                disk_used = int(disk_total * (20 + (i * 3) % 60 + (days_ago % 5) * 2) / 100)
                
                metric, created = NetworkMetric.objects.get_or_create(
                    equipment=equipment,
                    timestamp=timestamp,
                    defaults={
                        "cpu_usage": min(cpu_usage, 100),
                        "ping_response_time": ping_time,
                        "packet_loss": min(packet_loss, 100),
                        "bandwidth_up": (i + 1) * 1000000 + hour * 100000,
                        "bandwidth_down": (i + 1) * 10000000 + hour * 1000000,
                        "memory_total": memory_total,
                        "memory_used": memory_used,
                        "disk_total": disk_total,
                        "disk_used": disk_used,
                        "is_online": packet_loss < 50,  # Offline si trop de perte
                        "connection_quality": "excellent" if packet_loss < 1 else "good" if packet_loss < 5 else "fair" if packet_loss < 20 else "poor",
                    }
                )
    
    print(f"  ✅ Métriques créées pour {len(equipments[:10])} équipements sur 7 jours")
    
    # 7. Créer des alertes
    print("🚨 Création des alertes...")
    # Mapper les types d'alertes
    alert_type_mapping = {
        "critical": "error",
        "warning": "warning", 
        "info": "info"
    }
    
    alert_types = ["critical", "warning", "info"]
    alert_statuses = ["active", "acknowledged", "resolved"]
    alert_titles = [
        "CPU usage élevé",
        "Mémoire insuffisante", 
        "Espace disque faible",
        "Température élevée",
        "Perte de connectivité",
        "Maintenance requise",
        "Redémarrage nécessaire",
        "Mise à jour disponible",
    ]
    alert_messages = [
        "CPU usage élevé détecté sur l'équipement",
        "Mémoire insuffisante, risque de ralentissement",
        "Espace disque faible, nettoyage recommandé",
        "Température élevée détectée",
        "Perte de connectivité réseau intermittente",
        "Maintenance programmée requise",
        "Redémarrage système recommandé",
        "Mise à jour sécurité disponible",
    ]
    
    for i, equipment in enumerate(equipments[:15]):  # Alertes pour les 15 premiers équipements
        for j in range(2, 5):  # 2 à 4 alertes par équipement
            days_ago = j * 2 + (i % 3)
            title = alert_titles[j % len(alert_titles)]
            message = alert_messages[j % len(alert_messages)]
            
            alert, created = Alert.objects.get_or_create(
                equipment=equipment,
                title=title,
                message=message,
                defaults={
                    "type": alert_type_mapping.get(alert_types[j % len(alert_types)], "warning"),
                    "status": alert_statuses[j % len(alert_statuses)],
                    "resolved_at": timezone.now() - timedelta(days=days_ago//2) if j % 4 == 0 else None,
                }
            )
            if created:
                print(f"  ✅ Alerte créée: {alert.type} - {alert.title}")
    
    # 8. Statistiques finales
    print("\n📈 Statistiques des données créées:")
    print(f"  👥 Entreprises: {Company.objects.count()}")
    print(f"  👤 Utilisateurs: {User.objects.count()}")
    print(f"  🏢 Sites: {Site.objects.count()}")
    print(f"  🖥️  Équipements: {Equipment.objects.count()}")
    print(f"  📊 Métriques: {NetworkMetric.objects.count()}")
    print(f"  ⚠️  Seuils d'alerte: {AlertThreshold.objects.count()}")
    print(f"  🚨 Alertes: {Alert.objects.count()}")
    
    print("\n✅ Données de test créées avec succès!")
    print("\n🔑 Comptes de test:")
    print("  - admin / admin123 (superuser)")
    print("  - manager1 / password123 (TechCorp Solutions)")
    print("  - tech1 / password123 (TechCorp Solutions)")
    print("  - admin2 / password123 (IndustrieMax)")
    print("  - operator1 / password123 (SecureNet)")

if __name__ == "__main__":
    create_test_data()