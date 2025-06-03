from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import UserSerializer, UserRegisterSerializer, CompanySerializer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Récupérer l'utilisateur à partir du nom d'utilisateur dans la requête
            username = request.data.get('username')
            user = User.objects.get(username=username)
            response.data['user'] = UserSerializer(user).data
        return response

class UserProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'company']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    def get_queryset(self):
        # Les utilisateurs ne peuvent voir que les utilisateurs de leur entreprise
        return User.objects.filter(company=self.request.user.company)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un utilisateur"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'Utilisateur activé'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        if user == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas vous désactiver vous-même'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = False
        user.save()
        return Response({'status': 'Utilisateur désactivé'})

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Les utilisateurs ne peuvent voir que leur propre entreprise
        return Company.objects.filter(id=self.request.user.company.id)
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Récupérer tous les utilisateurs de l'entreprise"""
        company = self.get_object()
        users = company.users.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Statistiques de l'entreprise"""
        company = self.get_object()
        stats = {
            'total_users': company.users.count(),
            'active_users': company.users.filter(is_active=True).count(),
            'total_sites': company.sites.count(),
            'total_equipment': sum(site.equipment.count() for site in company.sites.all()),
            'active_equipment': sum(
                site.equipment.filter(status='active').count() 
                for site in company.sites.all()
            )
        }
        return Response(stats)
