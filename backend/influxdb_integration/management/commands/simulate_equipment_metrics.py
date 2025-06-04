"""
Commande Django pour simuler des métriques d'équipement.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from equipment.models import Equipment
from influxdb_integration.services import EquipmentMetricsService
import time
import random


class Command(BaseCommand):
    help = 'Simule des métriques pour tous les équipements'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Intervalle entre les mesures en secondes (défaut: 60)'
        )
        parser.add_argument(
            '--duration',
            type=int,
            default=3600,
            help='Durée totale de la simulation en secondes (défaut: 3600 = 1h)'
        )
        parser.add_argument(
            '--equipment-id',
            type=int,
            help='ID spécifique d\'un équipement à simuler'
        )
    
    def handle(self, *args, **options):
        interval = options['interval']
        duration = options['duration']
        equipment_id = options.get('equipment_id')
        
        if equipment_id:
            equipments = Equipment.objects.filter(id=equipment_id)
            if not equipments.exists():
                self.stdout.write(self.style.ERROR(f'Équipement {equipment_id} non trouvé'))
                return
        else:
            equipments = Equipment.objects.all()
        
        if not equipments.exists():
            self.stdout.write(self.style.WARNING('Aucun équipement trouvé'))
            return
        
        self.stdout.write(self.style.SUCCESS(
            f'Simulation démarrée pour {equipments.count()} équipement(s)'
        ))
        self.stdout.write(f'Intervalle: {interval}s, Durée: {duration}s')
        
        start_time = time.time()
        iterations = 0
        
        try:
            while time.time() - start_time < duration:
                for equipment in equipments:
                    # Simuler un changement de statut occasionnel
                    if random.random() < 0.05:  # 5% de chance
                        old_status = equipment.status
                        statuses = ['online', 'offline', 'warning']
                        statuses.remove(old_status)
                        equipment.status = random.choice(statuses)
                        equipment.save()
                        self.stdout.write(
                            f'Statut changé: {equipment.name} {old_status} -> {equipment.status}'
                        )
                    
                    # Enregistrer les métriques
                    EquipmentMetricsService.simulate_equipment_metrics(equipment)
                
                iterations += 1
                self.stdout.write(f'Itération {iterations} complétée')
                
                # Attendre avant la prochaine itération
                if time.time() - start_time < duration:
                    time.sleep(interval)
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nSimulation interrompue'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nSimulation terminée: {iterations} itérations effectuées'
        ))