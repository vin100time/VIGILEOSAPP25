from django.db import migrations

def create_test_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Company = apps.get_model('users', 'Company')
    
    # Récupérer les entreprises
    try:
        logistique = Company.objects.get(name="Entreprise de Logistique")
        banque = Company.objects.get(name="Groupe Bancaire")
        magasins = Company.objects.get(name="Chaîne de Magasins")
        
        # Sites pour l'entreprise de logistique (Paul)
        Site.objects.get_or_create(
            name="Agence Paris",
            defaults={
                'address': "25 rue de la Logistique, 75001 Paris",
                'company': logistique,
                'status': 'online'
            }
        )
        
        Site.objects.get_or_create(
            name="Agence Lyon",
            defaults={
                'address': "10 avenue des Transports, 69000 Lyon",
                'company': logistique,
                'status': 'online'
            }
        )
        
        Site.objects.get_or_create(
            name="Agence Marseille",
            defaults={
                'address': "5 boulevard Maritime, 13000 Marseille",
                'company': logistique,
                'status': 'warning'
            }
        )
        
        # Sites pour le groupe bancaire (Sophie)
        Site.objects.get_or_create(
            name="Agence Lille",
            defaults={
                'address': "30 rue des Finances, 59000 Lille",
                'company': banque,
                'status': 'online'
            }
        )
        
        Site.objects.get_or_create(
            name="Agence Bordeaux",
            defaults={
                'address': "15 cours Bancaire, 33000 Bordeaux",
                'company': banque,
                'status': 'offline'
            }
        )
        
        Site.objects.get_or_create(
            name="Agence Nantes",
            defaults={
                'address': "8 quai des Investissements, 44000 Nantes",
                'company': banque,
                'status': 'online'
            }
        )
        
        # Sites pour la chaîne de magasins (Karim)
        Site.objects.get_or_create(
            name="Magasin Toulouse",
            defaults={
                'address': "20 allée du Commerce, 31000 Toulouse",
                'company': magasins,
                'status': 'online'
            }
        )
        
        Site.objects.get_or_create(
            name="Magasin Nice",
            defaults={
                'address': "12 promenade des Achats, 06000 Nice",
                'company': magasins,
                'status': 'warning'
            }
        )
        
        Site.objects.get_or_create(
            name="Magasin Strasbourg",
            defaults={
                'address': "5 place du Marché, 67000 Strasbourg",
                'company': magasins,
                'status': 'online'
            }
        )
        
        # Site détecté pour test
        Site.objects.get_or_create(
            name="Nouveau Site Détecté",
            defaults={
                'address': "1 rue Inconnue, 75000 Paris",
                'company': logistique,
                'status': 'pending'
            }
        )
    except Company.DoesNotExist:
        pass

def delete_test_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('users', '0003_create_test_users'),
    ]

    operations = [
        migrations.RunPython(create_test_sites, delete_test_sites),
    ] 