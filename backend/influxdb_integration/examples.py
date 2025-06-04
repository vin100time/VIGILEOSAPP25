"""
Exemples d'utilisation du module InfluxDB Integration

Ce fichier contient des exemples pratiques pour utiliser l'intégration InfluxDB
dans différents contextes de l'application VIGILEOSAPP25.
"""

from datetime import datetime, timedelta
from influxdb_integration.services import EquipmentMetricsService, EquipmentAnalyticsService
from equipment.models import Equipment
from alerts.models import Alert


# ==============================================================================
# EXEMPLE 1 : Enregistrement de métriques basiques
# ==============================================================================

def example_basic_metrics():
    """Exemple d'enregistrement de métriques simples"""
    service = EquipmentMetricsService()
    
    # Enregistrer une température
    service.record_metric(
        equipment_id=1,
        metric_type='temperature',
        value=23.5,
        tags={
            'sensor': 'temp_sensor_01',
            'location': 'server_room',
            'unit': 'celsius'
        }
    )
    
    # Enregistrer la consommation électrique
    service.record_metric(
        equipment_id=1,
        metric_type='power_consumption',
        value=450.0,
        tags={
            'unit': 'watts',
            'phase': 'total'
        }
    )
    
    print("Métriques enregistrées avec succès")


# ==============================================================================
# EXEMPLE 2 : Monitoring de performance
# ==============================================================================

def example_performance_monitoring():
    """Exemple de monitoring de performance d'équipement"""
    service = EquipmentMetricsService()
    
    # Simuler des métriques de performance
    equipment_id = 1
    
    # Enregistrer les performances actuelles
    service.record_performance(
        equipment_id=equipment_id,
        cpu_usage=65.3,
        memory_usage=78.2,
        response_time=125.0
    )
    
    # Enregistrer des métriques réseau supplémentaires
    service.record_metric(
        equipment_id=equipment_id,
        metric_type='network_bandwidth',
        value=850.5,  # Mbps
        tags={
            'interface': 'eth0',
            'direction': 'inbound'
        }
    )
    
    service.record_metric(
        equipment_id=equipment_id,
        metric_type='disk_usage',
        value=82.1,  # Pourcentage
        tags={
            'mount_point': '/var',
            'filesystem': 'ext4'
        }
    )
    
    print("Métriques de performance enregistrées")


# ==============================================================================
# EXEMPLE 3 : Analyse de disponibilité
# ==============================================================================

def example_availability_analysis():
    """Exemple d'analyse de disponibilité sur une période"""
    analytics = EquipmentAnalyticsService()
    
    # Analyser la disponibilité du mois dernier
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    equipment_id = 1
    
    # Calculer la disponibilité
    availability = analytics.calculate_availability(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time
    )
    
    print(f"Disponibilité sur 30 jours : {availability:.2f}%")
    
    # Obtenir l'historique des statuts
    status_history = analytics.get_status_history(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time
    )
    
    print("\nHistorique des changements de statut :")
    for change in status_history:
        print(f"  {change['time']}: {change['previous_status']} → {change['new_status']}")


# ==============================================================================
# EXEMPLE 4 : Génération d'alertes basées sur les tendances
# ==============================================================================

def example_trend_based_alerts():
    """Exemple de création d'alertes basées sur l'analyse des tendances"""
    analytics = EquipmentAnalyticsService()
    
    # Analyser tous les équipements opérationnels
    for equipment in Equipment.objects.filter(status='operational'):
        # Analyser les 7 derniers jours
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        # Obtenir les statistiques de performance
        stats = analytics.get_performance_stats(
            equipment_id=equipment.id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Vérifier les seuils et créer des alertes si nécessaire
        alerts_created = []
        
        # CPU élevé
        if stats.get('cpu_avg', 0) > 80:
            alert = Alert.objects.create(
                equipment=equipment,
                alert_type='performance',
                severity='warning' if stats['cpu_avg'] < 90 else 'critical',
                message=f"Utilisation CPU élevée : {stats['cpu_avg']:.1f}% en moyenne sur 7 jours",
                is_active=True
            )
            alerts_created.append(alert)
        
        # Mémoire élevée
        if stats.get('memory_avg', 0) > 85:
            alert = Alert.objects.create(
                equipment=equipment,
                alert_type='performance',
                severity='warning' if stats['memory_avg'] < 95 else 'critical',
                message=f"Utilisation mémoire élevée : {stats['memory_avg']:.1f}% en moyenne",
                is_active=True
            )
            alerts_created.append(alert)
        
        # Temps de réponse dégradé
        if stats.get('response_time_avg', 0) > 500:  # ms
            alert = Alert.objects.create(
                equipment=equipment,
                alert_type='performance',
                severity='warning',
                message=f"Temps de réponse dégradé : {stats['response_time_avg']:.0f}ms en moyenne",
                is_active=True
            )
            alerts_created.append(alert)
        
        if alerts_created:
            print(f"\n{len(alerts_created)} alertes créées pour {equipment.name}")
            for alert in alerts_created:
                print(f"  - {alert.severity}: {alert.message}")


# ==============================================================================
# EXEMPLE 5 : Rapport de performance détaillé
# ==============================================================================

def example_detailed_performance_report():
    """Exemple de génération d'un rapport de performance détaillé"""
    analytics = EquipmentAnalyticsService()
    
    # Période d'analyse
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    equipment_id = 1
    equipment = Equipment.objects.get(id=equipment_id)
    
    print(f"\n{'='*60}")
    print(f"RAPPORT DE PERFORMANCE - {equipment.name}")
    print(f"Période : {start_time.strftime('%Y-%m-%d')} à {end_time.strftime('%Y-%m-%d')}")
    print(f"{'='*60}\n")
    
    # Disponibilité
    availability = analytics.calculate_availability(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time
    )
    print(f"Disponibilité : {availability:.2f}%")
    
    # Statistiques de performance
    stats = analytics.get_performance_stats(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time
    )
    
    print("\nPerformances moyennes :")
    print(f"  - CPU : {stats.get('cpu_avg', 0):.1f}% (min: {stats.get('cpu_min', 0):.1f}%, max: {stats.get('cpu_max', 0):.1f}%)")
    print(f"  - Mémoire : {stats.get('memory_avg', 0):.1f}% (min: {stats.get('memory_min', 0):.1f}%, max: {stats.get('memory_max', 0):.1f}%)")
    print(f"  - Temps de réponse : {stats.get('response_time_avg', 0):.0f}ms")
    
    # Métriques personnalisées
    metrics = analytics.get_equipment_metrics(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time,
        metric_type='temperature'
    )
    
    if metrics:
        temps = [m['value'] for m in metrics]
        avg_temp = sum(temps) / len(temps)
        print(f"\nTempérature moyenne : {avg_temp:.1f}°C")
        print(f"  - Min : {min(temps):.1f}°C")
        print(f"  - Max : {max(temps):.1f}°C")


# ==============================================================================
# EXEMPLE 6 : Monitoring en temps réel avec callback
# ==============================================================================

def example_realtime_monitoring():
    """Exemple de monitoring en temps réel avec traitement des données"""
    import time
    import random
    
    service = EquipmentMetricsService()
    analytics = EquipmentAnalyticsService()
    
    equipment_id = 1
    
    print("Démarrage du monitoring en temps réel (Ctrl+C pour arrêter)...")
    
    try:
        while True:
            # Simuler la collecte de métriques
            cpu = random.uniform(20, 80)
            memory = random.uniform(40, 90)
            temp = random.uniform(20, 35)
            
            # Enregistrer les métriques
            service.record_performance(
                equipment_id=equipment_id,
                cpu_usage=cpu,
                memory_usage=memory,
                response_time=random.uniform(50, 200)
            )
            
            service.record_metric(
                equipment_id=equipment_id,
                metric_type='temperature',
                value=temp,
                tags={'sensor': 'cpu_temp'}
            )
            
            # Vérifier les seuils en temps réel
            if cpu > 70:
                print(f"⚠️  CPU élevé : {cpu:.1f}%")
            if memory > 80:
                print(f"⚠️  Mémoire élevée : {memory:.1f}%")
            if temp > 30:
                print(f"🌡️  Température élevée : {temp:.1f}°C")
            
            print(f"✓ Métriques enregistrées - CPU: {cpu:.1f}%, Mem: {memory:.1f}%, Temp: {temp:.1f}°C")
            
            time.sleep(5)  # Attendre 5 secondes
            
    except KeyboardInterrupt:
        print("\nMonitoring arrêté")


# ==============================================================================
# EXEMPLE 7 : Export de données pour analyse externe
# ==============================================================================

def example_data_export():
    """Exemple d'export de données pour analyse externe"""
    import pandas as pd
    from datetime import datetime, timedelta
    
    analytics = EquipmentAnalyticsService()
    
    # Période d'export
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    # Collecter les données pour tous les équipements
    all_data = []
    
    for equipment in Equipment.objects.all():
        # Obtenir les métriques
        metrics = analytics.get_equipment_metrics(
            equipment_id=equipment.id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Ajouter les informations de l'équipement
        for metric in metrics:
            metric['equipment_id'] = equipment.id
            metric['equipment_name'] = equipment.name
            metric['equipment_type'] = equipment.equipment_type
            metric['site'] = equipment.site.name
            all_data.append(metric)
    
    # Créer un DataFrame
    df = pd.DataFrame(all_data)
    
    if not df.empty:
        # Sauvegarder en CSV
        filename = f"equipment_metrics_{start_time.strftime('%Y%m%d')}_{end_time.strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"Données exportées vers {filename}")
        
        # Afficher un résumé
        print(f"\nRésumé de l'export :")
        print(f"  - Période : {start_time.date()} à {end_time.date()}")
        print(f"  - Nombre d'équipements : {df['equipment_id'].nunique()}")
        print(f"  - Nombre total de métriques : {len(df)}")
        print(f"  - Types de métriques : {', '.join(df['metric_type'].unique())}")
    else:
        print("Aucune donnée à exporter")


# ==============================================================================
# EXEMPLE 8 : Intégration avec les tâches Celery
# ==============================================================================

def example_celery_task():
    """Exemple de tâche Celery pour la collecte périodique de métriques"""
    from celery import shared_task
    
    @shared_task
    def collect_all_equipment_metrics():
        """Collecte les métriques de tous les équipements actifs"""
        service = EquipmentMetricsService()
        
        success_count = 0
        error_count = 0
        
        for equipment in Equipment.objects.filter(status='operational'):
            try:
                # Simuler la collecte de métriques (remplacer par vraie collecte)
                import random
                
                service.record_performance(
                    equipment_id=equipment.id,
                    cpu_usage=random.uniform(10, 90),
                    memory_usage=random.uniform(20, 95),
                    response_time=random.uniform(50, 500)
                )
                
                # Métriques supplémentaires selon le type d'équipement
                if equipment.equipment_type == 'server':
                    service.record_metric(
                        equipment_id=equipment.id,
                        metric_type='disk_io',
                        value=random.uniform(0, 1000),  # IOPS
                        tags={'type': 'read'}
                    )
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Erreur pour {equipment.name}: {str(e)}")
        
        return {
            'success': success_count,
            'errors': error_count,
            'timestamp': datetime.now().isoformat()
        }
    
    # Exemple d'utilisation
    result = collect_all_equipment_metrics.delay()
    print(f"Tâche lancée avec ID : {result.id}")


# ==============================================================================
# Fonction principale pour exécuter les exemples
# ==============================================================================

if __name__ == "__main__":
    import sys
    
    examples = {
        '1': ('Métriques basiques', example_basic_metrics),
        '2': ('Monitoring de performance', example_performance_monitoring),
        '3': ('Analyse de disponibilité', example_availability_analysis),
        '4': ('Alertes basées sur les tendances', example_trend_based_alerts),
        '5': ('Rapport de performance détaillé', example_detailed_performance_report),
        '6': ('Monitoring temps réel', example_realtime_monitoring),
        '7': ('Export de données', example_data_export),
        '8': ('Tâche Celery', example_celery_task),
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in examples:
        name, func = examples[sys.argv[1]]
        print(f"\nExécution : {name}\n")
        func()
    else:
        print("\nExemples disponibles :")
        for key, (name, _) in examples.items():
            print(f"  {key}: {name}")
        print("\nUtilisation : python examples.py <numéro>")
        print("Exemple : python examples.py 1")