from django.db import models
from equipment.models import Equipment

class Alert(models.Model):
    TYPE_CHOICES = [
        ('error', 'Erreur'),
        ('warning', 'Avertissement'),
        ('info', 'Information'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Reconnue'),
        ('resolved', 'Résolue'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="alerts", verbose_name="Équipement")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='warning', verbose_name="Type")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Résolu le")
    
    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"
    
    def __str__(self):
        return self.title
