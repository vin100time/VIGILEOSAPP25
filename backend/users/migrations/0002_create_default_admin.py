from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_admin(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Company = apps.get_model('users', 'Company')
    
    # Créer une entreprise par défaut
    company, created = Company.objects.get_or_create(
        name="Vigileos Admin",
        defaults={
            'address': "1 rue de l'Administration, 75000 Paris"
        }
    )
    
    # Créer un utilisateur administrateur
    User.objects.get_or_create(
        username="admin",
        defaults={
            'email': "admin@vigileos.com",
            'password': make_password("admin123"),  # Mot de passe sécurisé à changer en production
            'is_staff': True,
            'is_superuser': True,
            'company': company,
            'first_name': "Admin",
            'last_name': "Vigileos"
        }
    )

def delete_default_admin(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(username="admin").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_admin, delete_default_admin),
    ] 