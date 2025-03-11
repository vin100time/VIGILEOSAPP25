from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_test_users(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Company = apps.get_model('users', 'Company')
    
    # Créer les entreprises
    logistique, _ = Company.objects.get_or_create(
        name="Entreprise de Logistique",
        defaults={
            'address': "15 avenue de la Logistique, 75001 Paris"
        }
    )
    
    banque, _ = Company.objects.get_or_create(
        name="Groupe Bancaire",
        defaults={
            'address': "25 rue de la Finance, 59000 Lille"
        }
    )
    
    magasins, _ = Company.objects.get_or_create(
        name="Chaîne de Magasins",
        defaults={
            'address': "8 boulevard du Commerce, 31000 Toulouse"
        }
    )
    
    # Créer les utilisateurs
    User.objects.get_or_create(
        username="paul",
        defaults={
            'email': "paul@logistique.fr",
            'password': make_password("paul123"),
            'is_staff': False,
            'is_superuser': False,
            'company': logistique,
            'first_name': "Paul",
            'last_name': "Dupont",
            'phone': "0123456789"
        }
    )
    
    User.objects.get_or_create(
        username="sophie",
        defaults={
            'email': "sophie@banque.fr",
            'password': make_password("sophie123"),
            'is_staff': False,
            'is_superuser': False,
            'company': banque,
            'first_name': "Sophie",
            'last_name': "Martin",
            'phone': "0234567890"
        }
    )
    
    User.objects.get_or_create(
        username="karim",
        defaults={
            'email': "karim@magasins.fr",
            'password': make_password("karim123"),
            'is_staff': False,
            'is_superuser': False,
            'company': magasins,
            'first_name': "Karim",
            'last_name': "Benali",
            'phone': "0345678901"
        }
    )

def delete_test_users(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(username__in=["paul", "sophie", "karim"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_default_admin'),
    ]

    operations = [
        migrations.RunPython(create_test_users, delete_test_users),
    ] 