from rest_framework import status, permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import (
    UserSerializer, UserCreateSerializer, UserRegisterSerializer, 
    UserUpdateSerializer, UserProfileSerializer, CompanySerializer,
    LoginSerializer, ChangePasswordSerializer
)

User = get_user_model()


class LoginView(APIView):
    """Vue pour l'authentification des utilisateurs."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """Vue pour l'inscription des utilisateurs."""
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


class LogoutView(APIView):
    """Vue pour la déconnexion des utilisateurs."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vue personnalisée pour l'obtention de tokens JWT."""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
                response.data['user'] = UserSerializer(user).data
            except User.DoesNotExist:
                pass
        return response


class UserProfileView(APIView):
    """Vue pour le profil utilisateur."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Vue pour changer le mot de passe."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Mot de passe modifié avec succès"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'company', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']
    ordering = ['username']
    
    def get_queryset(self):
        """Filtre les utilisateurs selon les permissions."""
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        elif user.company:
            return User.objects.filter(company=user.company)
        else:
            return User.objects.filter(id=user.id)
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        """Personnalise la création d'utilisateur."""
        # Si l'utilisateur n'est pas staff, assigne automatiquement son entreprise
        if not self.request.user.is_staff and self.request.user.company:
            serializer.save(company=self.request.user.company)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Active un utilisateur."""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'Utilisateur activé'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactive un utilisateur."""
        user = self.get_object()
        if user == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas vous désactiver vous-même'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = False
        user.save()
        return Response({'message': 'Utilisateur désactivé'})
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retourne les informations de l'utilisateur connecté."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des utilisateurs."""
        queryset = self.get_queryset()
        stats = {
            'total_users': queryset.count(),
            'active_users': queryset.filter(is_active=True).count(),
            'inactive_users': queryset.filter(is_active=False).count(),
            'staff_users': queryset.filter(is_staff=True).count(),
            'users_by_company': dict(
                queryset.values('company__name')
                .annotate(count=Count('id'))
                .values_list('company__name', 'count')
            )
        }
        return Response(stats)


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des entreprises."""
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filtre les entreprises selon les permissions."""
        user = self.request.user
        if user.is_staff:
            return Company.objects.all()
        elif user.company:
            return Company.objects.filter(id=user.company.id)
        else:
            return Company.objects.none()
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Récupère tous les utilisateurs de l'entreprise."""
        company = self.get_object()
        users = company.users.all()
        
        # Pagination
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def sites(self, request, pk=None):
        """Récupère tous les sites de l'entreprise."""
        company = self.get_object()
        sites = company.sites.all()
        
        # Import local pour éviter les imports circulaires
        from sites.serializers import SiteSerializer
        
        page = self.paginate_queryset(sites)
        if page is not None:
            serializer = SiteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Statistiques de l'entreprise."""
        company = self.get_object()
        
        # Calculs des statistiques
        total_sites = company.sites.count()
        total_equipment = sum(site.equipment.count() for site in company.sites.all())
        total_alerts = sum(
            sum(equipment.alerts.count() for equipment in site.equipment.all())
            for site in company.sites.all()
        )
        active_alerts = sum(
            sum(equipment.alerts.filter(status='active').count() for equipment in site.equipment.all())
            for site in company.sites.all()
        )
        
        stats = {
            'total_users': company.users.count(),
            'active_users': company.users.filter(is_active=True).count(),
            'total_sites': total_sites,
            'total_equipment': total_equipment,
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'equipment_by_status': {},
            'sites_by_status': {},
            'alerts_by_type': {}
        }
        
        # Statistiques détaillées si demandées
        if request.query_params.get('detailed', 'false').lower() == 'true':
            from django.db.models import Count
            from equipment.models import Equipment
            from sites.models import Site
            from alerts.models import Alert
            
            # Équipements par statut
            equipment_stats = Equipment.objects.filter(
                site__company=company
            ).values('status').annotate(count=Count('id'))
            stats['equipment_by_status'] = {
                item['status']: item['count'] for item in equipment_stats
            }
            
            # Sites par statut
            site_stats = Site.objects.filter(
                company=company
            ).values('status').annotate(count=Count('id'))
            stats['sites_by_status'] = {
                item['status']: item['count'] for item in site_stats
            }
            
            # Alertes par type
            alert_stats = Alert.objects.filter(
                equipment__site__company=company
            ).values('type').annotate(count=Count('id'))
            stats['alerts_by_type'] = {
                item['type']: item['count'] for item in alert_stats
            }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def my_company(self, request):
        """Retourne l'entreprise de l'utilisateur connecté."""
        if request.user.company:
            serializer = self.get_serializer(request.user.company)
            return Response(serializer.data)
        return Response(
            {'error': 'Aucune entreprise associée'}, 
            status=status.HTTP_404_NOT_FOUND
        )
