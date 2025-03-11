from rest_framework import viewsets
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    
    def get_queryset(self):
        # Filtrer les équipements par l'entreprise de l'utilisateur
        return Equipment.objects.filter(site__company=self.request.user.company)
