from rest_framework import viewsets
from .models import Alert
from .serializers import AlertSerializer

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    
    def get_queryset(self):
        # Filtrer les alertes par l'entreprise de l'utilisateur
        return Alert.objects.filter(equipment__site__company=self.request.user.company)
