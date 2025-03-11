from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Site
from .serializers import SiteSerializer
from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer

class SiteViewSet(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    
    def get_queryset(self):
        # Filtrer les sites par l'entreprise de l'utilisateur
        return Site.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        # Assigner automatiquement l'entreprise de l'utilisateur
        serializer.save(company=self.request.user.company)
    
    @action(detail=True)
    def equipment(self, request, pk=None):
        site = self.get_object()
        equipments = Equipment.objects.filter(site=site)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)
