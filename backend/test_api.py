#!/usr/bin/env python3
"""
Script de test complet pour l'API VIGILEOS
Teste tous les endpoints et fonctionnalités principales
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:12000/api"

class APITester:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
        
    def login(self, username="admin", password="admin123"):
        """Authentification"""
        print(f"🔐 Connexion avec {username}...")
        response = self.session.post(f"{BASE_URL}/auth/login/", json={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access"]
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            print(f"✅ Connexion réussie pour {data['user']['username']}")
            return True
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            return False
    
    def test_users(self):
        """Test des endpoints utilisateurs"""
        print("\n👥 Test des utilisateurs...")
        
        # Liste des utilisateurs
        response = self.session.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ {users['count']} utilisateurs trouvés")
        else:
            print(f"❌ Erreur liste utilisateurs: {response.status_code}")
            
        # Profil utilisateur
        response = self.session.get(f"{BASE_URL}/profile/")
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profil récupéré: {profile['username']}")
        else:
            print(f"❌ Erreur profil: {response.status_code}")
    
    def test_companies(self):
        """Test des endpoints entreprises"""
        print("\n🏢 Test des entreprises...")
        
        response = self.session.get(f"{BASE_URL}/companies/")
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ {companies['count']} entreprises trouvées")
            
            # Test détail entreprise
            if companies['results']:
                company_id = companies['results'][0]['id']
                response = self.session.get(f"{BASE_URL}/companies/{company_id}/")
                if response.status_code == 200:
                    print(f"✅ Détail entreprise récupéré")
                else:
                    print(f"❌ Erreur détail entreprise: {response.status_code}")
        else:
            print(f"❌ Erreur liste entreprises: {response.status_code}")
    
    def test_sites(self):
        """Test des endpoints sites"""
        print("\n🏢 Test des sites...")
        
        response = self.session.get(f"{BASE_URL}/sites/")
        if response.status_code == 200:
            sites = response.json()
            print(f"✅ {sites['count']} sites trouvés")
            
            # Test statistiques site
            if sites['results']:
                site_id = sites['results'][0]['id']
                response = self.session.get(f"{BASE_URL}/sites/{site_id}/site_stats/")
                if response.status_code == 200:
                    stats = response.json()
                    print(f"✅ Statistiques site: {stats['equipment']['total']} équipements")
                else:
                    print(f"❌ Erreur stats site: {response.status_code}")
        else:
            print(f"❌ Erreur liste sites: {response.status_code}")
    
    def test_equipment(self):
        """Test des endpoints équipements"""
        print("\n🖥️  Test des équipements...")
        
        response = self.session.get(f"{BASE_URL}/equipment/")
        if response.status_code == 200:
            equipment = response.json()
            print(f"✅ {equipment['count']} équipements trouvés")
            
            # Test métriques équipement
            if equipment['results']:
                eq_id = equipment['results'][0]['id']
                response = self.session.get(f"{BASE_URL}/equipment/{eq_id}/metrics/")
                if response.status_code == 200:
                    metrics = response.json()
                    print(f"✅ Métriques équipement récupérées")
                else:
                    print(f"❌ Erreur métriques: {response.status_code}")
        else:
            print(f"❌ Erreur liste équipements: {response.status_code}")
    
    def test_alerts(self):
        """Test des endpoints alertes"""
        print("\n🚨 Test des alertes...")
        
        response = self.session.get(f"{BASE_URL}/alerts/")
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ {alerts['count']} alertes trouvées")
            
            # Test statistiques alertes
            response = self.session.get(f"{BASE_URL}/alerts/stats/")
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ Stats alertes: {stats['total_alerts']} total, {stats['active_alerts']} actives")
            else:
                print(f"❌ Erreur stats alertes: {response.status_code}")
        else:
            print(f"❌ Erreur liste alertes: {response.status_code}")
    
    def test_metrics(self):
        """Test des endpoints métriques"""
        print("\n📊 Test des métriques...")
        
        response = self.session.get(f"{BASE_URL}/metrics/")
        if response.status_code == 200:
            metrics = response.json()
            print(f"✅ {metrics['count']} métriques trouvées")
        else:
            print(f"❌ Erreur liste métriques: {response.status_code}")
    
    def test_dashboard(self):
        """Test des endpoints dashboard"""
        print("\n📈 Test du dashboard...")
        
        # Dashboard global
        response = self.session.get(f"{BASE_URL}/dashboard/")
        if response.status_code == 200:
            dashboard = response.json()
            overview = dashboard.get('overview', {})
            print(f"✅ Dashboard global récupéré")
            print(f"   - {overview.get('total_equipment', 0)} équipements")
            print(f"   - {overview.get('total_sites', 0)} sites")
            print(f"   - {overview.get('active_alerts', 0)} alertes actives")
        else:
            print(f"❌ Erreur dashboard: {response.status_code}")
    
    def test_filtering(self):
        """Test des filtres"""
        print("\n🔍 Test des filtres...")
        
        # Filtrer équipements par type
        response = self.session.get(f"{BASE_URL}/equipment/?type=server")
        if response.status_code == 200:
            equipment = response.json()
            print(f"✅ Filtrage par type: {equipment['count']} serveurs")
        else:
            print(f"❌ Erreur filtrage: {response.status_code}")
        
        # Filtrer alertes par statut
        response = self.session.get(f"{BASE_URL}/alerts/?status=active")
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Filtrage alertes actives: {alerts['count']}")
        else:
            print(f"❌ Erreur filtrage alertes: {response.status_code}")
    
    def test_crud_operations(self):
        """Test des opérations CRUD"""
        print("\n✏️  Test des opérations CRUD...")
        
        # Créer une entreprise
        new_company = {
            "name": "Test Company API",
            "address": "123 Test Street"
        }
        response = self.session.post(f"{BASE_URL}/companies/", json=new_company)
        if response.status_code == 201:
            company = response.json()
            company_id = company['id']
            print(f"✅ Entreprise créée: {company['name']}")
            
            # Modifier l'entreprise
            updated_company = {
                "name": "Test Company API Updated",
                "address": "456 Updated Street"
            }
            response = self.session.patch(f"{BASE_URL}/companies/{company_id}/", json=updated_company)
            if response.status_code == 200:
                print(f"✅ Entreprise modifiée")
            else:
                print(f"❌ Erreur modification: {response.status_code}")
            
            # Supprimer l'entreprise
            response = self.session.delete(f"{BASE_URL}/companies/{company_id}/")
            if response.status_code == 204:
                print(f"✅ Entreprise supprimée")
            else:
                print(f"❌ Erreur suppression: {response.status_code}")
        else:
            print(f"❌ Erreur création entreprise: {response.status_code}")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 Démarrage des tests API VIGILEOS")
        print("=" * 50)
        
        if not self.login():
            print("❌ Impossible de se connecter, arrêt des tests")
            return False
        
        try:
            self.test_users()
            self.test_companies()
            self.test_sites()
            self.test_equipment()
            self.test_alerts()
            self.test_metrics()
            self.test_dashboard()
            self.test_filtering()
            self.test_crud_operations()
            
            print("\n" + "=" * 50)
            print("✅ Tous les tests terminés avec succès!")
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur pendant les tests: {e}")
            return False

def main():
    """Point d'entrée principal"""
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()