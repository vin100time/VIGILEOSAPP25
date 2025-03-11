from django.db import models
from sites.models import Site

class Equipment(models.Model):
    TYPE_CHOICES = [
        ('camera', 'Caméra'),
        ('video-recorder', 'Enregistreur vidéo'),
        ('switch', 'Switch'),
        ('server', 'Serveur'),
        ('access_point', 'Point d\'accès WiFi'),
        ('router', 'Routeur'),
        ('pc', 'PC'),
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('online', 'En ligne'),
        ('offline', 'Hors ligne'),
        ('warning', 'Attention'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="equipment", verbose_name="Site")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online', verbose_name="Statut")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Adresse IP")
    last_maintenance = models.DateField(null=True, blank=True, verbose_name="Dernière maintenance")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"
    
    def __str__(self):
        return self.name
