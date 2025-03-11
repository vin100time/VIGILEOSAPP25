from django.db import models
from users.models import Company

class Site(models.Model):
    STATUS_CHOICES = [
        ('online', 'En ligne'),
        ('offline', 'Hors ligne'),
        ('warning', 'Attention'),
        ('pending', 'Nouveau site détecté'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    address = models.TextField(verbose_name="Adresse")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sites", verbose_name="Entreprise")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"
    
    def __str__(self):
        return self.name
