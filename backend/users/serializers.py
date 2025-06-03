from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Company

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    """Serializer pour les entreprises."""
    users_count = serializers.SerializerMethodField()
    sites_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'created_at', 'users_count', 'sites_count']
        read_only_fields = ['created_at']
    
    def get_users_count(self, obj):
        """Retourne le nombre d'utilisateurs de l'entreprise."""
        return obj.users.count()
    
    def get_sites_count(self, obj):
        """Retourne le nombre de sites de l'entreprise."""
        return obj.sites.count()


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs."""
    company = CompanySerializer(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'company', 'company_name', 'phone', 'is_active', 
            'is_staff', 'date_joined', 'last_login', 'full_name'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur."""
        return f"{obj.first_name} {obj.last_name}".strip()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateurs."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'company', 'phone'
        ]
    
    def validate(self, attrs):
        """Valide que les mots de passe correspondent."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        """Crée un nouvel utilisateur."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserRegisterSerializer(UserCreateSerializer):
    """Alias pour la compatibilité."""
    pass


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour des utilisateurs."""
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'company', 'phone', 'is_active'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour le changement de mot de passe."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Valide que les nouveaux mots de passe correspondent."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        """Valide l'ancien mot de passe."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer pour l'authentification."""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Valide les identifiants de connexion."""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError("Identifiants invalides.")
            
            if not user.is_active:
                raise serializers.ValidationError("Compte utilisateur désactivé.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Nom d'utilisateur et mot de passe requis.")


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur."""
    company_details = CompanySerializer(source='company', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'company_details', 'date_joined', 'last_login',
            'full_name'
        ]
        read_only_fields = ['username', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur."""
        return f"{obj.first_name} {obj.last_name}".strip()
