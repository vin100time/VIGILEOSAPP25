from django.db import models
from equipment.models import Equipment

class NetworkMetric(models.Model):
    """Métriques réseau time-series pour les équipements"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="metrics")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Métriques réseau
    ping_response_time = models.FloatField(null=True, blank=True, help_text="Temps de réponse ping en ms")
    packet_loss = models.FloatField(null=True, blank=True, help_text="Perte de paquets en %")
    bandwidth_up = models.BigIntegerField(null=True, blank=True, help_text="Bande passante montante en bps")
    bandwidth_down = models.BigIntegerField(null=True, blank=True, help_text="Bande passante descendante en bps")
    
    # Métriques système
    cpu_usage = models.FloatField(null=True, blank=True, help_text="Utilisation CPU en %")
    memory_total = models.BigIntegerField(null=True, blank=True, help_text="Mémoire totale en bytes")
    memory_used = models.BigIntegerField(null=True, blank=True, help_text="Mémoire utilisée en bytes")
    disk_total = models.BigIntegerField(null=True, blank=True, help_text="Espace disque total en bytes")
    disk_used = models.BigIntegerField(null=True, blank=True, help_text="Espace disque utilisé en bytes")
    
    # Métriques de connectivité
    is_online = models.BooleanField(default=True)
    connection_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Bon'),
            ('fair', 'Moyen'),
            ('poor', 'Mauvais'),
            ('offline', 'Hors ligne'),
        ],
        default='good'
    )
    
    class Meta:
        verbose_name = "Métrique réseau"
        verbose_name_plural = "Métriques réseau"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['equipment', '-timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['is_online']),
        ]
    
    def __str__(self):
        return f"{self.equipment.name} - {self.timestamp}"

    @property
    def memory_usage_percent(self):
        """Calcule le pourcentage d'utilisation mémoire"""
        if self.memory_total and self.memory_used:
            return (self.memory_used / self.memory_total) * 100
        return None
    
    @property
    def disk_usage_percent(self):
        """Calcule le pourcentage d'utilisation disque"""
        if self.disk_total and self.disk_used:
            return (self.disk_used / self.disk_total) * 100
        return None

class AlertThreshold(models.Model):
    """Seuils d'alerte pour les métriques"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="thresholds")
    
    # Seuils réseau
    ping_warning_threshold = models.FloatField(default=100.0, help_text="Seuil d'avertissement ping en ms")
    ping_critical_threshold = models.FloatField(default=500.0, help_text="Seuil critique ping en ms")
    packet_loss_warning = models.FloatField(default=5.0, help_text="Seuil d'avertissement perte paquets en %")
    packet_loss_critical = models.FloatField(default=20.0, help_text="Seuil critique perte paquets en %")
    
    # Seuils système
    cpu_warning_threshold = models.FloatField(default=80.0, help_text="Seuil d'avertissement CPU en %")
    cpu_critical_threshold = models.FloatField(default=95.0, help_text="Seuil critique CPU en %")
    memory_warning_threshold = models.FloatField(default=80.0, help_text="Seuil d'avertissement mémoire en %")
    memory_critical_threshold = models.FloatField(default=95.0, help_text="Seuil critique mémoire en %")
    disk_warning_threshold = models.FloatField(default=80.0, help_text="Seuil d'avertissement disque en %")
    disk_critical_threshold = models.FloatField(default=95.0, help_text="Seuil critique disque en %")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Seuil d'alerte"
        verbose_name_plural = "Seuils d'alerte"
        unique_together = ['equipment']
    
    def __str__(self):
        return f"Seuils - {self.equipment.name}"
